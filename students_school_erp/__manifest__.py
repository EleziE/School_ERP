{
    'name': 'Students',
    'data': [
        # Security
        'security/ir.model.access.csv',
        # Wizards
        'wizards/suspend_reason_wizard.xml',
        # Views
        'views/students.xml',
        'views/student_subject.xml',
        # Menu
        'views/menu.xml',
    ],
    'depends': [
        'base_school_erp',
        'mail',
    ],
    'icon': 'students_school_erp/static/description/icon.png',
    'web_icon': 'students_school_erp,static/description/icon.png',
    'assets': {
        'web.assets_backend': [
            'students_school_erp/static/src/css/student_form.css',
        ],
    }
}
