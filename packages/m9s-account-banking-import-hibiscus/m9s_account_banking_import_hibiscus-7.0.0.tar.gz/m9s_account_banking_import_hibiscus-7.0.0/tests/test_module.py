# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.tests.test_tryton import ModuleTestCase


class AccountBankingImportHibiscusTestCase(ModuleTestCase):
    "Test Account Banking Import Hibiscus module"
    module = 'account_banking_import_hibiscus'


del ModuleTestCase
