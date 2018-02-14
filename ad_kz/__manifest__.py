{
    'name': "ad_kz",

    'summary': """
        Модуль справочников""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base',"mail"],
    'data': [
        'views/task_kz.xml',

        'views/partner.xml',
        'views/menu.xml',
        # 'data/client_grouplist.csv'
    ],
    'application': True,
}
