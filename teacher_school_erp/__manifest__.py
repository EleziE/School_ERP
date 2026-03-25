{
    'name':'Teacher',

    'data':[
        # Security
        'security/ir.model.access.csv',
        # Data
        'data/teacher_seq.xml',
        # Inherited
        'views/inherited/teacher_view_users_simple_form_inherited.xml',
        'views/student_inherited.xml',
        # Views
        'views/teacher_view.xml',
    ],
    'depends':['base_school_erp','students_school_erp'],
    'icon': 'teacher_school_erp/static/description/icon.png',
}