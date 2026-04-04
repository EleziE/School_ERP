{
    'name': 'Students',
    'data': [
        # Security
        'security/ir.model.access.csv',
        # Wizards
        'wizards/suspend_reason_wizard.xml',
        # Sequence
        'data/seq_student.xml',
        # Views
        'views/students.xml',
        'views/menu.xml',
    ],
    'depends': [
        'base_school_erp',
    ],
    'icon': 'students_school_erp/static/description/icon.png',
    'web_icon': 'students_school_erp,static/description/icon.png',
}
