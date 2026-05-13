{
    'name': 'Configurations',
    'description': """Configurations School ERP""",
    'license': 'LGPL-3',
    'data': [
        # Security
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        # Data
        'data/year_data.xml',
        'data/semester_data.xml',
        # Inherited
        # 'views/Inherited/costume_base_modifications.xml', #doesnt work because the modules that are hidden should also be inside the 'depends'
        # Sequences
        # Views
        'views/holidays.xml',
        'views/classroom.xml',
        'views/subjects.xml',
        'views/exam.xml',
        'views/faculty.xml',
        'views/year.xml',
        'views/semester.xml',
        'views/menu.xml', ],
    'icon': 'configurations_school_erp/static/description/icon.png',
    'assets': {
        'web.assets_backend': [
            'configurations_school_erp/static/src/css/app_center.css',
        ],
    }
}
