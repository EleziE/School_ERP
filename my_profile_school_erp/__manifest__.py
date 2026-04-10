{
    'name': 'My Profile',
    'depends': [
        'base_school_erp',
        'students_school_erp',
        'teacher_school_erp',
        'task_school_erp',
        'finance_school_erp',
    ],
    'data': [
        # Security
        'security/ir.model.access.csv',
        # Teacher Views
        'views/teacher/my_profile_teacher.xml',
        'views/teacher/my_tasks_teacher.xml',
        # Student Views
        'views/student/my_profile_student.xml',
        'views/student/my_finances_student.xml',
        # Menu-item's
        'views/menu.xml',
    ],
    'icon': 'my_profile_school_erp/static/description/icon.png',
    'web_icon': 'my_profile_school_erp,static/description/icon.png',
}
