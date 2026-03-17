{
    'name': 'Task',
    'data': [
        # Security
        'security/ir.model.access.csv',
        # Views
        'views/task.xml',
        'views/teacher_inherit.xml',
    ],
    'application': True,
    'installable': True,
    "depends": ['teacher_school_erp'],
    'icon': 'task_school_erp/static/description/icon.png',
    'web_icon': 'task_school_erp,static/description/icon.png',
}
