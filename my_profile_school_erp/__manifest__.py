{
    'name': 'My Profile',
    'depends': [
        'base_school_erp',
        'students_school_erp',
        'teacher_school_erp',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/my_profile_student.xml',
        'views/my_profile_teacher.xml',
        'views/menu.xml',
    ],
}
