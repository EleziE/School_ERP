{
    'name':'Teacher',

    'data':[
        # Security
        'security/ir.model.access.csv',
        # Wizard
        'views/wizards_view/assign_subject_teacher_wizard.xml',
        # Inherited
        'views/wizards_view/res_user_inherited.xml',
        # Views
        'views/teacher_view.xml',
        'views/student_inherit_view.xml',
    ],
    'depends':['base_school_erp','students_school_erp']
}