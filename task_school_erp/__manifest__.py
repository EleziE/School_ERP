{
    'name': 'Task',
    'data': [
        # Security
        'security/ir.model.access.csv',
        'security/rules.xml',
        #Data
        'data/seq_task.xml',
        # Views
        'views/task.xml',
        'views/Inherited/(teacher)task_notebook.xml',
        'views/menu.xml',
    ],
    'application': True,
    'installable': True,
    "depends": [
        'base_school_erp',
        'teacher_school_erp',
        'administration_school_erp',
    ],
    'icon': 'task_school_erp/static/description/icon.png',
    'web_icon': 'task_school_erp,static/description/icon.png',
}
