{
    'name': 'My Profile',
    'depends': [
        'base',
        'base_school_erp',
        'student_school_erp',
        'teacher_school_erp',
    ],
    'application': True,
    'installable': True,
    'icon': 'my_profil_school_erp/static/description/icon.png',
    'web_icon': 'my_profil_school_erp/static/description/icon.png',
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
    ]
}
