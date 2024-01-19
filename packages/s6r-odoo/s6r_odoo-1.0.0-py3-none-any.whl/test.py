from s6r_odoo import OdooConnection

odoo_cli = OdooConnection(url='http://odoo_digitalportage.localhost',
                          dbname='digitalportage_preprod',
                          user='admin',
                          password='admin')
partners = odoo_cli.read_search('res.partner', [])
for partner in partners:
    print(partner)
