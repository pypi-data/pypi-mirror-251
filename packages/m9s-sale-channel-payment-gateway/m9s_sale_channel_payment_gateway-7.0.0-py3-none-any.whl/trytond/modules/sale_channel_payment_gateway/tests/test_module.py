# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.tests.test_tryton import ModuleTestCase


class SaleChannelPaymentGatewayTestCase(ModuleTestCase):
    "Test Sale Channel Payment Gateway module"
    module = 'sale_channel_payment_gateway'


del ModuleTestCase
