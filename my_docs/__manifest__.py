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
        'views/task.xml',
        'views/reglament.xml',
        'views/menu.xml',
        'views/session_workflow.xml',

        # 'data/client_grouplist.csv'
    ],
    'application': True,
}
