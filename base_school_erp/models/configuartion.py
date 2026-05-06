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


class Exams(models.Model):
    _name = 'exams'
    _description = 'Exams'

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


class Faculty(models.Model):
    _name = 'faculty.faculty'
    _description = 'Faculty'
    _rec_name = 'name'

    name = fields.Char(string='Faculty Name', required=True)
    code = fields.Char(string='Code', required=True)
    max_year = fields.Integer(string='Max Years')
    sequence = fields.Char(string='Sequence', readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('sequence', _('New')) == _('New'):
                # Get the code entered by the user or API (e.g., 'cs', 'med')
                faculty_code = vals.get('code')

                if faculty_code:
                    # Dynamically construct the sequence code
                    # e.g. 'faculty.cs' or 'faculty.medicine'
                    seq_code = f'faculty.{faculty_code}'

                    # Check if this sequence exists
                    sequence = self.env['ir.sequence'].search([('code', '=', seq_code)], limit=1)

                    if not sequence:
                        # OPTIONAL: Automatically create the sequence if it's missing
                        sequence = self.env['ir.sequence'].create({
                            'name': f'Sequence for {vals.get("name")}',
                            'code': seq_code,
                            'prefix': f'{faculty_code.upper()}-',
                            'padding': 3,
                        })

                    vals['sequence'] = sequence.next_by_id()
                else:
                    # Fallback to a generic sequence if no code is provided
                    vals['sequence'] = self.env['ir.sequence'].next_by_code('faculty.faculty') or _('New')

        return super().create(vals_list)


class Year(models.Model):
    _name = 'year.year'
    _description = 'Year'
    _rec_name = 'name'
    _order = 'order asc'

    name = fields.Char(string='Year', required=True)
    code = fields.Char(string='Code', required=True)
    order = fields.Integer(string='Order')


class Semester(models.Model):
    _name = 'semester.semester'
    _description = 'Semester'
    _rec_name = 'name'
    _order = 'order asc'

    year_id = fields.Many2one('year.year')
    name = fields.Char(string='Semester', required=True)
    code = fields.Char(string='Code', required=True)
    order = fields.Integer(string='Order')


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


class Subject(models.Model):
    _name = 'subject.subject'
    _description = 'Subject'

    sequence = fields.Char(string='Sequence', readonly=True)
    name = fields.Char(string='Subject name')
    faculty_id = fields.Many2one(comodel_name='faculty.faculty', string='Faculty')
    year_id = fields.Many2one(comodel_name='year.year', string='Year')
    semester_id = fields.Many2one(comodel_name='semester.semester', string='Semester')
    type = fields.Selection(selection=[('mandatory', 'Mandatory'),
                                       ('selective', 'Selective'),
                                       ('faculty_elective', 'Faculty Elective'),
                                       ('university_elective', 'University Elective'), ],
                            string='Type', required=True)
    credits = fields.Integer(string='Credits')
    description = fields.Html(string='Description')

    @api.onchange('faculty_id')
    def _onchange_faculty_id(self):
        if self.year_id and self.faculty_id:
            if self.year_id.order > self.faculty_id.max_year:
                self.year_id = False
        return {'domain': {'year_id': [('order', '<=', self.faculty_id.max_year or 5)]}}

    @api.model_create_multi
    def create(self, vals_list):
        codes = {
            'cs': 'subject.cs',
            'medicine': 'subject.med',
            'engineering': 'subject.engineering',
            'social': 'subject.social',
            'laws': 'subject.laws',
            'economic': 'subject.economic',
            'architecture': 'subject.architecture',
            'arts': 'subject.arts',
            'education': 'subject.education',
            'pharmacy': 'subject.pharmacy',
            'foreign_language': 'subject.foreign_language',
            'dentist': 'subject.dentist',
        }
        for vals in vals_list:
            if vals.get('sequence', _('New')) == _('New'):
                faculty_id = vals.get('faculty_id')
                faculty_code = self.env['faculty.faculty'].browse(faculty_id).code if faculty_id else None
                code = codes.get(faculty_code, 'subject.subject')
                vals['sequence'] = self.env['ir.sequence'].next_by_code(code) or _('New')
        return super().create(vals_list)

    _sql_constraints = [
        ('seq_uq', 'UNIQUE(sequence)', "Sequence already exists !"),
    ]
