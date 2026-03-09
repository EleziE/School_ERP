{
    'name': 'Library Book Manager',
    'version': '17.0.1.0.0',
    'category': 'Services',
    'author': 'Enes',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/library_category_views.xml',
        'views/library_books_views.xml',
        'views/library_borrow_views.xml',
        'views/library_member_views.xml', ],
    'installable': True,
    'application': True,
}
