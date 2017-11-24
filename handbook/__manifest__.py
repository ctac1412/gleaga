{
    'name': "tech_directory",

    'summary': """
        Модуль справочников""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base',"mail"],
    'data': [
        'views/reglament.xml',
        'views/client.xml',
        'views/grouplist.xml',
        'views/manager.xml',
        'views/contractor.xml',
        'views/doc_package.xml',
        'views/own_company.xml',
        'views/dogovor.xml',
        'views/dop_dogovor.xml',
        'views/extra_service.xml',
        'views/supplier.xml',
        # 'data/tech_directory_grouplist.csv'
    ],
    'application': True,
}
