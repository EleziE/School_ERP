{
    'name': "Hospital",
    'version': '1.0.0',
    'category': 'Custom',
    'summary': 'A mini-system for the hospital',
    'author': 'Enes',
    'data': [
        # Security

        # Testing git

        'security/ir.model.access.csv',

        # Views
        'views/appointments_view.xml',
        'views/medicaments_view.xml',
        'views/patient_view.xml',
        'views/doctors_view.xml',

        # Patient-only

        # MainMenu (menu-items)
        'views/menu.xml',
    ],
    'depends': ['mail'],
    'installable': True,
    'auto_install': True,
    'sequence': 0,
}
