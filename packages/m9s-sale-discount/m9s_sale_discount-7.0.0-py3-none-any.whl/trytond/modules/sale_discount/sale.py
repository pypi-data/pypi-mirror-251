# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from decimal import Decimal

from trytond.model import fields
from trytond.modules.account_invoice_discount.invoice import (
    discount_digits, gross_unit_price_digits)
from trytond.modules.currency.fields import Monetary
from trytond.modules.product import round_price
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval
from trytond.transaction import Transaction

STATES = {
    'invisible': Eval('type') != 'line',
    'required': Eval('type') == 'line',
    'readonly': Eval('sale_state') != 'draft',
    }


class Sale(metaclass=PoolMeta):
    __name__ = 'sale.sale'
    sale_discount = fields.Numeric('Sale Discount',
        digits=discount_digits, states={
            'readonly': Eval('state') != 'draft',
            },
        help='This discount will be applied in all lines after their own '
        'discount.')

    @classmethod
    def __setup__(cls):
        super().__setup__()
        if not cls.lines.context:
            cls.lines.context = {}
        cls.lines.context['sale_discount'] = Eval('sale_discount')
        cls.lines.depends.add('sale_discount')
        # The following helps to avoid corrupted function field context on
        # workers (#4591)
        #cls.lines.context['company'] = Eval('company')
        #cls.lines.depends.add('company')

    @staticmethod
    def default_sale_discount():
        return Decimal(0)

    @classmethod
    def write(cls, *args):
        actions = iter(args)
        sales_todo = []
        for sales, _ in zip(actions, actions):
            sales_todo.extend(sales)
        super().write(*args)
        if Transaction().context.get('apply_discount_to_lines', True):
            cls.apply_discount_to_lines(sales_todo)

    @classmethod
    def create(cls, vlist):
        sales = super().create(vlist)
        if Transaction().context.get('apply_discount_to_lines', True):
            cls.apply_discount_to_lines(sales)
        return sales

    @classmethod
    def apply_discount_to_lines(cls, sales):
        Line = Pool().get('sale.line')
        to_write = []
        for sale in sales:
            for line in sale.lines:
                old_unit_price = line.unit_price
                old_discount = line.discount
                line.update_prices()
                if (old_unit_price != line.unit_price
                        or old_discount != line.discount):
                    to_write.append(line)
        if to_write:
            Line.save(to_write)

    def get_shipment_cost_line(self, carrier, cost, unit_price=None):
        # add gross unit price in sale shipment cost line
        cost_line = super().get_shipment_cost_line(carrier, cost, unit_price)
        cost_line.gross_unit_price = cost_line.unit_price
        cost_line.update_prices()
        return cost_line


class SaleLine(metaclass=PoolMeta):
    __name__ = 'sale.line'
    gross_unit_price = Monetary('Gross Price', digits=gross_unit_price_digits,
        currency='currency', states=STATES)
    discount = fields.Numeric('Discount', digits=discount_digits,
        states=STATES)

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls.unit_price.states['readonly'] = True

    @staticmethod
    def default_discount():
        return Decimal(0)

    @property
    def has_promotion(self):
        return (hasattr(self, 'promotion')
                and self.promotion
                and self.draft_unit_price)

    @fields.depends('sale', 'gross_unit_price', 'unit_price', 'discount',
        methods=['on_change_with_amount'])
    def update_prices(self):
        unit_price = None
        gross_unit_price = self.gross_unit_price
        sale_discount = Transaction().context.get('sale_discount')

        if sale_discount is None:
            if self.sale and hasattr(self.sale, 'sale_discount'):
                sale_discount = self.sale.sale_discount or Decimal(0)
            else:
                sale_discount = Decimal(0)

        if self.gross_unit_price is not None and (self.discount is not None
                or sale_discount is not None):
            unit_price = self.gross_unit_price
            if self.has_promotion:
                unit_price = self.draft_unit_price
            if self.discount:
                unit_price *= (1 - self.discount)
            if sale_discount:
                unit_price *= (1 - sale_discount)

            if self.discount and sale_discount:
                discount = (self.discount + sale_discount
                    - self.discount * sale_discount)
                if discount != 1:
                    gross_unit_price = unit_price / (1 - discount)
            elif self.discount and self.discount != 1:
                gross_unit_price = unit_price / (1 - self.discount)
            elif sale_discount and sale_discount != 1:
                gross_unit_price = unit_price / (1 - sale_discount)

            unit_price = round_price(unit_price)

            gup_digits = self.__class__.gross_unit_price.digits[1]
            gross_unit_price = gross_unit_price.quantize(
                Decimal(str(10.0 ** -gup_digits)))

        self.gross_unit_price = gross_unit_price
        if self.has_promotion:
            self.draft_unit_price = unit_price
        else:
            self.unit_price = unit_price
        self.amount = self.on_change_with_amount()

    @fields.depends('_parent_sale.sale_discount', 'discount')
    def on_change_unit(self):
        super().on_change_unit()

    @fields.depends(methods=['update_prices'])
    def on_change_gross_unit_price(self):
        self.update_prices()

    @fields.depends('unit_price', methods=['update_prices'])
    def on_change_unit_price(self):
        # unit_price has readonly state but could be set from source code
        if self.unit_price is not None:
            self.update_prices()

    @fields.depends('sale', methods=['update_prices'])
    def on_change_discount(self):
        self.update_prices()

    @fields.depends('discount', 'unit_price', '_parent_sale.sale_discount',
        methods=['update_prices'])
    def on_change_product(self):
        super().on_change_product()
        self.gross_unit_price = self.unit_price
        if self.discount is None:
            self.discount = Decimal(0)
        if self.unit_price is not None:
            self.update_prices()

    @fields.depends('discount', 'unit_price', '_parent_sale.sale_discount',
        methods=['update_prices'])
    def on_change_quantity(self):
        super().on_change_quantity()
        self.gross_unit_price = self.unit_price
        if not self.discount:
            self.discount = Decimal(0)
        if self.unit_price is not None:
            self.update_prices()

    def get_invoice_line(self):
        pool = Pool()
        InvoiceLine = pool.get('account.invoice.line')
        digits = InvoiceLine.discount.digits[1]

        lines = super().get_invoice_line()
        for line in lines:
            if not hasattr(line, 'gross_unit_price') or line.gross_unit_price is None:
                line.gross_unit_price = self.gross_unit_price
            discount = Decimal(0)
            if self.discount and self.sale and self.sale.sale_discount:
                discount = (Decimal('1.0')
                    - (Decimal('1.0') - self.discount)
                    * (Decimal('1.0') - self.sale.sale_discount))
            elif self.sale and self.sale.sale_discount:
                discount = self.sale.sale_discount
            elif self.discount:
                discount = self.discount
            line.discount = discount.quantize(Decimal(str(10.0 ** -digits)))
        return lines

    @classmethod
    def create(cls, vlist):
        Sale = Pool().get('sale.sale')
        vlist = [x.copy() for x in vlist]
        for vals in vlist:
            if vals.get('type', 'line') != 'line':
                continue
            if vals.get('unit_price') is None:
                vals['gross_unit_price'] = Decimal(0)
                continue

            if 'gross_unit_price' not in vals:
                gross_unit_price = vals['unit_price']
                if vals.get('discount') not in (None, 1):
                    gross_unit_price = (gross_unit_price
                        / (1 - vals['discount']))
                if vals.get('sale'):
                    sale = Sale(vals['sale'])
                    sale_discount = sale.sale_discount
                    if sale_discount not in (None, 1):
                        gross_unit_price = (gross_unit_price
                            / (1 - sale_discount))
                if gross_unit_price != vals['unit_price']:
                    digits = cls.gross_unit_price.digits[1]
                    gross_unit_price = gross_unit_price.quantize(
                        Decimal(str(10.0 ** -digits)))
                vals['gross_unit_price'] = gross_unit_price
            if not vals.get('discount'):
                vals['discount'] = Decimal(0)
        return super().create(vlist)
