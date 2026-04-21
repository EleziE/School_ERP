                                                                                                    ============4/3/2026============
---
RECHECK: A ka naj menyr tjeter si me e vendos ne notebook Subject perveq se me e vendos fieldin aty (m2m) .. me e ba si
me financen apo duhet per me ba modul tjeter SUBJECT per me e ba ashtu.

---

                                                                                        ######################## 4/8/2026 #########################
---
Recheck the previous questions

View Form of Task (make that the finished date to be editable only if the uid is the same as the id of the person that
the task is created),
and the statusbar to be editable to compleat only if the uid is the same as the created for id

                                                                                        ######################## 4/10/2026 #########################
---
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

Pse ne Task (logged as Admin) kur krijon task per Agim user te del butoni compleat ama per Fatmirin ose Hasanin nuk ban
HAHAAHAHAHA

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

                                                                                            ################## 4/11/2026 ##################

---
Pse ?
```py
        <menuitem id="students"
                  name="Students"
                  action="action_students"
                  web_icon='students_school_erp,static/description/icon.png'
                  groups="base_school_erp.group_school_admin"/>

                  
access_student_student_admin,access.student.admin,model_students_students,base_school_erp.group_school_admin,1,1,1,1
access_student_student_student,access.student.student,model_students_students,base_school_erp.group_school_student,1,0,0,0


######################## 4/14/2026 #########################
1.Per me e fsheh modulin Task ose Finance , mos noshta duhet me kriju modul tjeter i cili referon (related)
tek fiannca ose task edhe ..... nejse se noshta nuk dalin recordet sepse jan te rujtuna ne tabel tjeter...
######################## 4/15/2026 #########################
1.why the <chatter/> doesnt work in odoo 17
    and the old version it works

```xml

<div class="oe_chatter">
    <field name="message_follower_ids"/>
    <field name="activity_ids"/>
    <field name="message_ids"/>
</div>
```

3.the report (unpaid_finances) not getting recognized by the button in view

Pse si user student i can still see the module students ?



4.per cfar ndikojn kta dy rreshta ne my profile_student
member type edhe userid 

pse kur jan autofillen te dhenat ndersa kur nuk jan nuk autofillen

```xml

<group>
    <field name="member_type" invisible="True"/>
    <field name="user_id" invisible="True" readonly="True"
           domain="[('member_type','=','student')]" options="{'no_open':True}"/>
    <field name="sequence"/>
    <field name="name"/>
    <field name="surname"/>
    <field name="state"/>
    <field name="gender" readonly="True"/>
    <field name="enrollment_date" readonly="True"/>
</group>
```
                                                                                            ######################## 4/17/2026 #########################
# nr.100

Why the name of the person who set the state to paid is not being shown in the form view . Where is the error 

---
```python
def pay_finance(self): 
    self.write({
        'state': 'paid',
        'user_id': self.env.user.id,
    })
     
def pay_finance(self):
    self.state = 'paid'

# ne rast se du thejsht per status ... a bajn te dyja te njejten gja .. edhe pse ne write munem me fut edhe tjera gjana ne te 
```
---

Recheck in task why you cant enter the name of the teacher

                                                                                            ######################## 4/21/2026 #########################

These are all unfinished work. After work dont forget to delete the ones done

- CP-Commit #2 (04/21/2026)

To filter the m2m field after selecting the faculty name , year ,semester so the subject of the selected fields to me shown... is not working

- CP-Commit #3 (04/21/2026)

Wizard + Report 

Trying to make the button that select the state of finance than based on that the PDF report ot be created ...
the majority of the files created and added in this commit don't work

- CP-Commit #4 (04/21/2026)

Small changes, recheck the previous unsolved problems

- CP-Commit #5 (04/21/2026)

How to make a button that if the state of a student is graduated to not allow to sign in ... or the moment that he signs in to show only a page that tells e message as i want 

I have created a graduated_fella() boolean type function in the student model but how to connect it with the res_users... or to add it there 


In TASK module why the create_by is not filled by the uid ... learn the logic (form view ... creating a new task)

Recheck the sequence if it changes as it should after saving the autofilled version (the previous error)