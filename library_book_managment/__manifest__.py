{
    'name': 'Library Book Manager',
    'version': '17.0.1.0.0',
    'category': 'Services',
    'author': 'Enes',
    'depends': ['base','sale'],
    'data': [
        # security
        'security/ir.model.access.csv',
        # data
        'data/sequence.xml',
        # main views
        'views/root_views/root_menu.xml',
        'views/root_views/library_category_views.xml',
        'views/root_views/library_books_views.xml',
        'views/root_views/library_borrow_views.xml',
        'views/root_views/library_member_views.xml',
        # inherited views
        'views/inherited_views/library_books_extended_views.xml',
        'views/inherited_views/library_member_extended_views.xml',
        'views/inherited_views/library_borrow_extended_views.xml',
        'views/inherited_views/library_category_extended_views.xml',
        'views/inherited_views/res_partner_views.xml',
        'views/inherited_views/sale_order_views.xml',
        ],
    'installable': True,
    'application': True,
    'sequence':0,
}


