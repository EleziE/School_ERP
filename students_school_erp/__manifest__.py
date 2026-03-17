{
    'name': 'Students',
    'data': [
        # Security
        'security/ir.model.access.csv',
        # Wizards
        'wizards/suspend_reason_wizard.xml',
        # Inherited
        'views/student_user_form_view_inherited.xml',
        'views/students_user_form_base_inherited.xml',
        # Views
        'views/students.xml',
    ],
    'depends': [
        'base_school_erp',],
    'icon':'students_school_erp/static/description/icon.png',
    'web_icon':'students_school_erp,static/description/icon.png',
}
