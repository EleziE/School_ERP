Prap nuk ban me e ba usersin None (access rights)

============4/3/2026============

1.Pse ne students_students field email duhet me e ba Readonly = False per me dal ne view normal si duhet (ose te CP ma
bani ket pun).

2.Si me e parandalu kur nga state GRADUATED e qoj ne ACTIVE ose tjeter
graduated date me u ba invisible prap (kur ndryshohet prej ne db)

RECHECK: A ka naj menyr tjeter si me e vendos ne notebook Subject perveq se me e vendos fieldin aty (m2m) .. me e ba si
me financen apo duhet per me ba modul tjeter SUBJECT per me e ba ashtu.

3.Rishiko si me e ba per me marr te dhanat e sakta per my profile per staudent (e njejta edhe per teacher)

####################### 4/7/2026 ###############################
<field name="graduation_date" invisible=" not user_id and state != 'graduated'"/>

ne student form view, pse ne disa prej tyne edhe pse e kan sate != 'graduated' prap si field del (apo ngaqe kam ba
ndryshim ne db edhe ka met naj gja (prej ne graduated ne activ or whatever))

######################## 4/8/2026 #########################

Recheck the previous questions

View Form of Task (make that the finished date to be editable only if the uid is the same as the id of the person that the task is created),
and the statusbar to be editable to compleat only if the uid is the same as the created for id 

pse spunon buttoni print info the student erp from view (dicka e till) ku e ke ..
######################## 4/10/2026 #########################
            ### To-do #1 ###
```py
created_by = fields.Many2one(comodel_name='teacher.teacher',
                                 string='Created by',
                                 default=lambda self: self.env['teacher.teacher'].search(
                                     [('user_id', '=', self.env.uid)], limit=1),
                                 readonly=True)                
```
or 
```py
created_by = fields.Many2one(comodel_name='res.users',
                                 string='Created by',
                                 default=lambda self: self.env['teacher.teacher'].search(
                                     [('user_id', '=', self.env.uid)], limit=1),
                                 readonly=True)
```
Pse ne Task (logged as Admin) kur krijon task per Agim user te del butoni compleat ama per Fatmirin ose Hasanin nuk ban HAHAAHAHAHA

```python
    @api.model
def open_my_profile(self):
    """
    Return action that opens the logged-in teacher's profile
    Made with pure ChatGPT how I don't know hy hy hy
    """
    teacher = self.env['teacher.teacher'].search([('user_id', '=', self.env.uid)], limit=1)
    if not teacher:
        teacher = self.create({'user_id': self.env.uid})
    return {
        'type': 'ir.actions.act_window',
        'name': 'My Profile',
        'res_model': 'teacher.teacher',
        'res_id': teacher.id,
        'view_mode': 'form',
        'target': 'current',
        'views': [(self.env.ref('teacher_school_erp.teacher_form_view').id, 'form')],
    }


        'views': [(self.env.ref('teacher_school_erp.teacher_form_view').id, 'form')],
# ishte 
        'views': [(self.env.ref('teacher_school_erp.my_profile_teacher').id, 'form')],
# ca shkakton prb
```
######################## 4/14/2026 #########################
Per me e fsheh modulin Task ose Finance , mos noshta duhet me kriju modul tjeter i cili referon (related)
tek fiannca ose task edhe ..... nejse se noshta nuk dalin recordet sepse jan te rujtuna ne tabel tjeter...
################## 4/11/2026 ##################
Pse ?
```py
        <menuitem id="students"
                  name="Students"
                  action="action_students"
                  web_icon='students_school_erp,static/description/icon.png'
                  groups="base_school_erp.group_school_admin"/>

                  
access_student_student_admin,access.student.admin,model_students_students,base_school_erp.group_school_admin,1,1,1,1
access_student_student_student,access.student.student,model_students_students,base_school_erp.group_school_student,1,0,0,0


Pse si user student i can still see the module students ?
```

