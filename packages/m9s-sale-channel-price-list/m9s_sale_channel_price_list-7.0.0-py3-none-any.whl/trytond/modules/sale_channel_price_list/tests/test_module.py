# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.tests.test_tryton import ModuleTestCase


class SaleChannelPriceListTestCase(ModuleTestCase):
    "Test Sale Channel Price List module"
    module = 'sale_channel_price_list'


del ModuleTestCase
