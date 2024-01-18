# -*- coding: utf-8 -*-
{
  'name': "vertical_carsharing_rest_api",

  'summary': """
    Partner rest service""",

  'author': "Som Mobilitat",
  'website': "https://www.sommobilitat.coop",

  # Categories can be used to filter modules in modules listing
  # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
  # for the full list
  'category': 'vertical-carsharing',
  'version': '12.0.0.0.2',

  # any module necessary for this one to work correctly
  'depends': [
    'base',
    'easy_my_coop_api'
  ],

  # always loaded
  'data': [

  ],
  # only loaded in demonstration mode
  'demo': [],
}
