{
    'name': 'Base School ERP',
    'data': [
        # Security
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        # Inherited
        'views/Inherited/costume_base_modifications.xml',
        # Sequences
        'views/Sequence/subject_seq.xml',
        'views/Sequence/classroom_seq.xml',
        # Views
        'views/menu.xml',
        'views/holidays.xml',
        'views/classroom.xml',
        'views/subjects.xml',
        'views/exam.xml', ],
    'icon': 'base_school_erp/static/description/icon.png',
    'assets': {
        'web.assets_backend': [
            'base_school_erp/static/src/css/app_center.css',
        ],
    }

}
