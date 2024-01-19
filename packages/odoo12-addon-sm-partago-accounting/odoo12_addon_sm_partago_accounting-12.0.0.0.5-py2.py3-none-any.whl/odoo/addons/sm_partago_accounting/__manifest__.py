{
    'name': "sm_partago_accounting",

    'summary': """
    Module to manage app accounting integrated in odoo
  """,

    'author': "Som Mobilitat",
    'website': "https://www.sommobilitat.coop",

    'category': 'Uncategorized',
    'version': '12.0.0.0.5',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'vertical_carsharing',
        'sm_partago_db',
        'sm_partago_user',
        'account_asset_management',
    ],

    # always loaded
    'data': [
        'views/views_members.xml',
        'views/views_account_asset.xml'
    ],
    # only loaded in demonstration mode
    'demo': [],
}
