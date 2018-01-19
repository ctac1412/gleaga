{
    'name': "my_docs",

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
        'security/ir.model.access.csv',
        'security/access_rules.xml',
        'groups/groups.xml',
        'views/task.xml',
        'views/reglament.xml',
        'views/partner.xml',
        'views/menu.xml',
        'views/wizards.xml',
        'views/company.xml'


        # 'data/client_grouplist.csv'
    ],
    'application': True,
}
