{
    'name': 'Administration School',
    'license':'LGPL-3',
    'description':"""Administration School""",
    'data': [
        'security/ir.model.access.csv',
        'data/administration_seq.xml',
        'views/administration.xml',
        'views/menu.xml',
    ],
    'depends': [
        'base_school_erp',
        'base',
        'mail',
    ],
    'icon': 'administration_school_erp/static/description/icon.png',
}
