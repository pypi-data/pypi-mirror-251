# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.modules.company.tests import CompanyTestMixin
from trytond.tests.test_tryton import ModuleTestCase


class SalePriceWithTaxTestCase(CompanyTestMixin, ModuleTestCase):
    "Test Sale Price With Tax module"
    module = 'sale_price_with_tax'


del ModuleTestCase
