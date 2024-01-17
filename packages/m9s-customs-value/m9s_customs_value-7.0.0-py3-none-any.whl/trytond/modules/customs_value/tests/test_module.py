# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from decimal import Decimal

from trytond.pool import Pool
from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.transaction import Transaction
from trytond.modules.company.tests import (
    CompanyTestMixin, create_company, set_company)

def get_company():
    pool = Pool()
    Company = pool.get('company.company')

    companies = Company.search([])
    if companies:
        company = companies[0]
    else:
        company = create_company()
    return company


class CustomsValueTestCase(ModuleTestCase):
    'Test Customs Value module'
    module = 'customs_value'

    @with_transaction()
    def test0010_check_product_custom_value(self):
        """
        Check custom value for product
        """
        pool = Pool()
        Uom = pool.get('product.uom')
        Template = pool.get('product.template')
        Product = pool.get('product.product')

        company = get_company()

        with set_company(company):
            uom, = Uom.search([('name', '=', 'Unit')])
            template = Template(
                name='template',
                list_price=Decimal('20'),
                default_uom=uom,
                )
            template.save()

            product1 = Product(
                template=template,
                )
            product1.save()

            self.assertEqual(product1.use_list_price_as_customs_value, True)
            self.assertEqual(product1.customs_value_used, product1.list_price)

            product2 = Product(
                template=template,
                customs_value=Decimal('50'),
                use_list_price_as_customs_value=False,
                )
            product2.save()
            self.assertEqual(product2.use_list_price_as_customs_value, False)
            self.assertEqual(product2.customs_value_used, product2.customs_value)

            product2.use_list_price_as_customs_value = True
            product2.save()

            self.assertEqual(product2.use_list_price_as_customs_value, True)
            self.assertEqual(product2.customs_value_used, product2.list_price)

    @with_transaction()
    def test0020_check_product_customs_description(self):
        """
        Check customs description for product
        """
        pool = Pool()
        Uom = pool.get('product.uom')
        Template = pool.get('product.template')
        Product = pool.get('product.product')

        company = get_company()
        with set_company(company):
            uom, = Uom.search([('name', '=', 'Unit')])
            template = Template(
                name='template',
                list_price=Decimal('20'),
                default_uom=uom,
                )
            template.save()

            product1 = Product(
                template=template,
                )
            product1.save()

            self.assertEqual(product1.use_name_as_customs_description, True)
            self.assertEqual(product1.customs_description_used, product1.name)

            product2 = Product(
                template=template,
                customs_description="Customs Description",
                use_name_as_customs_description=False,
                )
            product2.save()

            self.assertEqual(product2.use_name_as_customs_description, False)
            self.assertEqual(product2.customs_description_used,
                product2.customs_description)

            product2.use_name_as_customs_description = True
            product2.save()

            self.assertEqual(product2.use_name_as_customs_description, True)
            self.assertEqual(product2.customs_description_used, product2.name)


del ModuleTestCase
