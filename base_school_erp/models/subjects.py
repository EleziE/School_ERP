from odoo import fields, models, api, _


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
                                       ('selective', 'Selective')],
                            string='Type',
                            required=True)
    credits = fields.Integer(string='Credits')

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
        # =================== Per Sequence Generator ===================

    _sql_constraints = [
        ('seq_uq', 'UNIQUE(sequence)', "Sequence already exists !"),
    ]
