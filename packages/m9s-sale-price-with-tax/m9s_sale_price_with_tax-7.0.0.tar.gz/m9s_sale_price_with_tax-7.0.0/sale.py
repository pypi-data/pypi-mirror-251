# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from decimal import Decimal

from trytond.model import fields
from trytond.modules.currency.fields import Monetary
from trytond.modules.product import price_digits
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval
from trytond.transaction import Transaction

_ZERO = Decimal('0.0')


class SaleLine(metaclass=PoolMeta):
    __name__ = 'sale.line'
    unit_price_w_tax = fields.Function(Monetary('Unit Price with Tax',
            digits=price_digits, currency='currency',
            states={
                'invisible': Eval('type') != 'line',
            }), 'get_price_with_tax')
    amount_w_tax = fields.Function(Monetary('Amount with Tax',
            digits='currency', currency='currency',
            states={
                'invisible': ~Eval('type').in_(['line', 'subtotal']),
            }), 'get_price_with_tax')

    @classmethod
    def get_price_with_tax(cls, lines, names):
        pool = Pool()
        Tax = pool.get('account.tax')
        amount_w_tax = {}
        unit_price_w_tax = {}

        def compute_amount_with_tax(line):
            tax_amount = _ZERO
            if line.taxes:
                tax_list = Tax.compute(line.taxes,
                    line.unit_price or _ZERO,
                    line.quantity or 0.0, line.tax_date)

                tax_amount = sum(
                    [t['amount'] for t in tax_list], _ZERO)
            return line.amount + tax_amount

        for line in lines:
            amount = _ZERO
            unit_price = _ZERO
            currency = line.sale.currency if line.sale else line.currency

            if line.type == 'line':
                if line.quantity and line.amount:
                    amount = compute_amount_with_tax(line)
                    unit_price = amount / Decimal(str(line.quantity))

            # Only compute subtotals if the two fields are provided to speed up
            elif line.type == 'subtotal' and len(names) == 2:
                for line2 in line.sale.lines:
                    if line2.type == 'line':
                        amount2 = compute_amount_with_tax(line2)
                        if currency:
                            amount2 = currency.round(amount2)
                        amount += amount2
                    elif line2.type == 'subtotal':
                        if line == line2:
                            break
                        amount = _ZERO

            if currency:
                amount = currency.round(amount)
            amount_w_tax[line.id] = amount
            unit_price_w_tax[line.id] = unit_price

        result = {
            'amount_w_tax': amount_w_tax,
            'unit_price_w_tax': unit_price_w_tax,
            }
        for key in list(result.keys()):
            if key not in names:
                del result[key]
        return result

    @fields.depends('type', 'unit_price', 'quantity',
        'taxes', 'sale', '_parent_sale.currency', 'currency', 'product',
        'amount')
    def on_change_with_unit_price_w_tax(self, name=None):
        if not self.sale:
            self.sale = Transaction().context.get('sale')
        return SaleLine.get_price_with_tax([self],
            ['unit_price_w_tax'])['unit_price_w_tax'][self.id]

    @fields.depends('type', 'unit_price', 'quantity',
        'taxes', 'sale', '_parent_sale.currency', 'currency', 'product',
        'amount')
    def on_change_with_amount_w_tax(self, name=None):
        if not self.sale:
            self.sale = Transaction().context.get('sale')
        return SaleLine.get_price_with_tax([self],
            ['amount_w_tax'])['amount_w_tax'][self.id]


class SaleLineDiscount(metaclass=PoolMeta):
    __name__ = 'sale.line'

    @fields.depends(methods=['on_change_with_unit_price_w_tax',
        'on_change_with_amount_w_tax'])
    def update_prices(self):
        super().update_prices()
        self.unit_price_w_tax = self.on_change_with_unit_price_w_tax()
        self.amount_w_tax = self.on_change_with_amount_w_tax()
