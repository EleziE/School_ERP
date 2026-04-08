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