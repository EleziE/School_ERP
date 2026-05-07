{
    'name': 'Teacher',
    'license': 'LGPL-3',
    'description': """Teacher""",
    'data': [
        # Security
        'security/ir.model.access.csv',
        #  Views
        'views/teacher_notebook.xml',
        'views/teacher_view.xml',
        'views/menu.xml',
    ],
    'depends': [
        'base_school_erp',
        'students_school_erp',
        'mail'
    ],
    'icon': 'teacher_school_erp/static/description/icon.png',
}
