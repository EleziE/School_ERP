{
    'name': 'Finance',
    'data': [
        # security
        'security/ir.model.access.csv',

        # Views
        'views/my_finance.xml',
        'views/finance.xml',
        'views/students_inherit.xml',

        # All menus (should be at the end before the actions)
        'views/menu.xml',
    ],
    'depends': [
        'base_school_erp',
        'students_school_erp', ],
    'icon': 'finance_school_erp/static/description/icon.png',
    'web_icon': 'finance_school_erp,static/description/icon.png',
}
