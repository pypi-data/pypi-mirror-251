# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.tests.test_tryton import ModuleTestCase


class AccountInvoiceDiscountTestCase(ModuleTestCase):
    "Test Account Invoice Discount module"
    module = 'account_invoice_discount'


del ModuleTestCase
