from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ResUsersInheritance(models.Model):
    _inherit = 'res.users'

    member_type = fields.Selection(selection=[('none', 'None'),
                                              ('student', 'Student'),
                                              ('teacher', 'Teacher'),
                                              ('administration', 'Administration'),
                                              ('admin', 'Admin'), ],
                                   store=True)


class Faculty(models.Model):
    _name = 'faculty.faculty'
    _description = 'Faculty'
    _rec_name = 'name'

    year_id = fields.Many2one(comodel_name='year.year')

    name = fields.Char(string='Faculty Name', )
    code = fields.Char(string='Code',
                       required=True,
                       help="It will be used like prefix latter for subject (e.g 'cs','med','arch')")
    year = fields.Integer(string='Years',
                          related='year_id.order',
                          help='How long the faculty will be normally ',
                          readonly=True,
                          store=True)

    @api.constrains('year')
    def _check_year(self):
        for rec in self:
            if not (2 <= rec.year <= 6):
                raise ValidationError('Year must be between 2 and 6')


class Year(models.Model):
    _name = 'year.year'
    _description = 'Year'
    _rec_name = 'name'
    _order = 'order asc'


    name = fields.Char(string='Year',
                       readonly=True)
    order = fields.Integer(string= 'Order',
                           help="Number of years, will be used by the other modules (e.g faculty)",
                           readonly=True, )
    code = fields.Char(string='Code',
                       readonly=True,
                       help="Pre-generated with the year_data")


class Semester(models.Model):
    _name = 'semester.semester'
    _description = 'Semester'
    _rec_name = 'name'
    _order = 'order asc'

    year_id = fields.Many2one(comodel_name='year.year')
    year = fields.Char(related='year_id.name', string='Year',store=True)
    name = fields.Char(string='Semester',
                       required=True)
    code = fields.Char(string='Code',
                       required=True)
    order = fields.Integer(string='Order')


class Subject(models.Model):
    _name = 'subject.subject'
    _description = 'Subject'

    faculty_id = fields.Many2one(comodel_name='faculty.faculty', string='Faculty')
    year_id = fields.Many2one(comodel_name='year.year', string='Year')
    semester_id = fields.Many2one(comodel_name='semester.semester', string='Semester')

    sequence = fields.Char(string='Sequence', readonly=True)
    name = fields.Char(string='Name')
    type = fields.Selection(selection=[('mandatory', 'Mandatory'),
                                       ('selective', 'Selective'),
                                       ('faculty_elective', 'Faculty Elective'),
                                       ('university_elective', 'University Elective'), ],
                            string='Type', required=True)
    credits = fields.Integer(string='Credits')
    description = fields.Html(string='Description')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('sequence', 'New') == 'New':
                # 1. Get the faculty code from the database
                faculty = self.env['faculty.faculty'].browse(vals.get('faculty_id'))
                # Fallback to 'GEN' if no faculty is linked
                f_code = faculty.code.upper() if faculty else 'GEN'

                # 2. Define the unique code for the ir.sequence record
                seq_key = f'subject.seq.{f_code.lower()}'

                # 3. Get the next number (creating the sequence if it doesn't exist)
                existing_seq = self.env['ir.sequence'].search([('code', '=', seq_key)], limit=1)

                if not existing_seq:
                    existing_seq = self.env['ir.sequence'].create({
                        'name': f'Subject Sequence for {f_code}',
                        'code': seq_key,
                        'prefix': f'{f_code}-',
                        'padding': 3,
                    })

                vals['sequence'] = existing_seq.next_by_id()

        return super().create(vals_list)

    _sql_constraints = [
        ('seq_uq', 'UNIQUE(sequence)', "Sequence already exists !"),
    ]


class Exams(models.Model):
    _name = 'exams'
    _description = 'Exams'

    faculty_id = fields.Many2one('faculty.faculty')
    semester_id = fields.Many2one('semester.semester')
    subject_id = fields.Many2one('subject.subject')
    year_id = fields.Many2one('year.year')

    faculty_years = fields.Integer(related='faculty_id.year',string='Faculty Years',store=True)
    name = fields.Char(string='Exam')
    date_of_exam = fields.Date(string='Date of exam')

    @api.constrains('date_of_exam')
    def _check_exam_holiday(self):
        for rec in self:
            holiday = self.env['holiday.holiday'].search([('date', '=', rec.date_of_exam)])
            if holiday:
                raise ValidationError(f"{holiday.name}, so please chose another date for the exam.")


class Holidays(models.Model):
    _name = 'holiday.holiday'
    _description = 'Holiday'

    name = fields.Char(string='Holidays name')
    date = fields.Date(string='Holidays date')


class ClassRooms(models.Model):
    _name = 'class.rooms'
    _description = 'Class Room'
    _rec_name = 'name'

    sequence = fields.Char(string='Sequence', readonly=True)
    name = fields.Char(string='Class name')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('sequence', _('New')) == _('New'):
                vals['sequence'] = self.env['ir.sequence'].next_by_code('class.rooms') or _('New')
        return super().create(vals_list)

    _sql_constraints = [
        ('seq_uq', 'UNIQUE(sequence)', "Sequence already exists !"),
    ]
