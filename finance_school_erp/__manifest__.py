{
    'name': 'Finance',
    'data': [
        # security
        'security/ir.model.access.csv',
        'security/rules.xml',

        # Wizards
        'wizards/finances_print_wizard.xml',

        # Views
        'views/finance.xml',

        # Inherited
        'views/Inherited/student_notebook.xml',

        # All menus (should be at the end before the actions)
        'views/menu.xml',
    ],
    'depends': [
        'base_school_erp',
        'students_school_erp',
        'teacher_school_erp',
        'mail',
        'administration_school_erp',
    ],
    'icon': 'finance_school_erp/static/description/icon.png',
    'web_icon': 'finance_school_erp,static/description/icon.png',
}
