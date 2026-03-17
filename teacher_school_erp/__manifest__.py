{
    'name':'Teacher',

    'data':[
        # Security
        'security/ir.model.access.csv',
        # Views
        'views/teacher_view.xml',
        'views/student_inherit_view.xml',
    ],
    'depends':['base_school_erp','students_school_erp'],
    'icon': 'teacher_school_erp/static/description/icon.png',
}