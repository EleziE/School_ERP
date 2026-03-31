{
    'name': 'Teacher',

    'data': [
        # Security
        'security/ir.model.access.csv',
        # Data
        'data/teacher_seq.xml',
        'views/teacher_notebook.xml',
        # Views
        'views/teacher_view.xml',
        'views/(Teacher)my_profile.xml',
        'views/menu.xml',
    ],
    'depends': ['base_school_erp', 'students_school_erp'],
    'icon': 'teacher_school_erp/static/description/icon.png',
}