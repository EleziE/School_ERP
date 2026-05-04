from odoo import fields, models,api,_
from odoo.exceptions import ValidationError


class ResUsersInheritance(models.Model):
    _inherit = 'res.users'

    member_type = fields.Selection(selection=[('none', 'None'),
                                              ('student', 'Student'),
                                              ('teacher', 'Teacher'),
                                              ('administration', 'Administration'),
                                              ('admin', 'Admin'), ],
                                   store=True)


class ClassRooms(models.Model):
    _name = 'class.rooms'
    _description = 'Class Room'
    _rec_name = 'name'

    sequence = fields.Char(string='Sequence',readonly=True)
    name = fields.Char(string='Class name')



    @api.model
    def create(self, vals):
        # =================== Per Sequence Generator ====================
        if vals.get('sequence', _('New')) == _('New'):
            vals['sequence'] = self.env['ir.sequence'].next_by_code('class.rooms') or _('New')
        # =================== Per Sequence Generator ===================
        return super().create(vals)

    _sql_constraints = [
        ('seq_uq', 'UNIQUE(sequence)', "Sequence already exists !"),
    ]


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


class Subject(models.Model):
    _name = 'subject.subject'
    _description = 'Subject'

    sequence = fields.Char(string='Sequence', readonly=True)
    name = fields.Char(string='Subject name')
    faculty = fields.Selection(selection=[('cs', 'Computer Science'),
                                          ('medicine', 'Medicine'),
                                          ('engineering', 'Engineering'),
                                          ('social', 'Social'),
                                          ('laws', 'Laws'),
                                          ('economic', 'Economic'),
                                          ('architecture', 'Architecture'),
                                          ('arts', 'Arts'),
                                          ('education', 'Education'),
                                          ('pharmacy', 'Pharmacy'),
                                          ('foreign_language', 'Foreign_language'),
                                          ('dentist', 'Dentist'), ],
                               string='Faculty', required=True)

    semester = fields.Selection(string='Semester', selection=[('semester-1', 'First Semester'),
                                                              ('semester-2', 'Second Semester'), ])
    year = fields.Selection(selection=[
        ('1st', 'First Year'),
        ('2nd', 'Second Year'),
        ('3rd', 'Third Year'), ],
        string='Year')
    type = fields.Selection(selection=[('mandatory', 'Mandatory'),
                                       ('selective', 'Selective'),
                                       ('faculty_elective', 'Faculty Elective'),
                                       ('university_elective', 'University Elective'),],
                            string='Type',
                            required=True)
    credits = fields.Integer(string='Credits')
    description = fields.Html(string='Description')

    @api.model
    def create(self, vals):
        # =================== Per Sequence Generator ====================
        if vals.get('sequence', _('New')) == _('New'):
            faculty = vals.get('faculty')
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
            code = codes.get(faculty, 'subject.subject')
            vals['sequence'] = self.env['ir.sequence'].next_by_code(code) or _('New')

        return super().create(vals)

    _sql_constraints = [
        ('seq_uq', 'UNIQUE(sequence)', "Sequence already exists !"),
    ]
