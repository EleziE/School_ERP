{
    'name': 'Finance',
    'data': [
        # security
        'security/ir.model.access.csv',

        # Views
        'wizards/finances_print.xml',
        'views/my_finance.xml',
        'views/finance.xml',
        'views/Inherited/student_notebook.xml',

        # All menus (should be at the end before the actions)
        'views/menu.xml',
    ],
    'depends': [
        'base_school_erp',
        'students_school_erp',
        'teacher_school_erp',
    ],
    'icon': 'finance_school_erp/static/description/icon.png',
    'web_icon': 'finance_school_erp,static/description/icon.png',
}
