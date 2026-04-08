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
        'security/ir.model.access.csv',
        'views/my_profile_teacher.xml',
        'views/my_profile_student.xml',
        'views/my_finances_student.xml',
        'views/menu.xml',
    ],
}
