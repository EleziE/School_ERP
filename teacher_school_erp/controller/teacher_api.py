from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request, Response
import json

class TeacherAPI(http.Controller):



######### GET API
    @http.route('/api/teacher/<int:teacher_id>',methods=['GET'], type='http', auth='public', csrf=False)
    def get_teacher_info(self, teacher_id):

            teacher = request.env['teacher.teacher'].browse(teacher_id)
            if not teacher.exists():
                return Response(
                json.dumps({'error': 'teacher not found'}),
                content_type="application/json",
                status=404
                )

            for teacher in teacher:
                data = {
                'id': teacher.id,
                'sequence': teacher.sequence,
                'name': teacher.name,
                'surname': teacher.surname,
                'email': teacher.email,
                'external_email': teacher.external_email,
                'phone': str(teacher.phone) if teacher.phone else None,
                'subject_id': teacher.subject_id.ids,
                'gender': teacher.gender,
                'member_type': teacher.member_type,
                }
            return Response(
            json.dumps(data),
                content_type="application/json",
                status=200)

    @http.route('/api/teacher/list_teacher', methods=['GET'], type='http', auth='public', csrf=False)
    def get_teacher_list(self):

            teacher = request.env['teacher.teacher'].search([])

            data = []
            for rec in teacher:
                data.append({
                'id': rec.id,
                'sequence': rec.sequence,
                'name': rec.name,
                'surname': rec.surname,
                'email': rec.email,
                'external_email': rec.external_email,
                'phone': rec.phone,
                'subject_id': rec.subject_id.ids,
                'gender': rec.gender,
                'member_type': rec.member_type,
            })
            return Response(
            json.dumps(data),
                content_type="application/json",
                status=200)



######### POST API
    @http.route('/api/teacher/create_teacher',methods=['POST'], type='http', auth='user', csrf=False)
    def create_teacher(self):
        """
        About the API key:

        Required fields: name and email should be filled and a unique email for every user ,
                         member type should always be Teacher !!!

        """
        try:
            data = json.loads(request.httprequest.data)

            if data.get('member_type') != 'teacher':
                error = 'This API is only for teacher creation (member type not correct )'
                return Response(
                json.dumps(error),content_type="application/json",status=400)

            if not data.get('name'):
                error = 'Name cannot be empty or NULL!'
                return Response(
                    json.dumps(error),content_type="application/json",status=400)

            if not data.get('email') :
                error = 'Email cannot be empty or NULL!'
                return Response(
                    json.dumps(error),content_type="application/json",status=400)

            if request.env['res.users'].search([('login','=',data.get('email'))]):
                error = 'Email already exists!'
                return Response(
                    json.dumps(error),content_type="application/json",status=400)

            teacher = request.env['teacher.teacher'].create({
            'name': data.get('name'),
            'surname': data.get('name'),
            'phone': data.get('phone'),
            'dob': data.get('dob'),
            'education': data.get('education'),
            'blood_type': data.get('blood_type'),
            'member_type': data.get('member_type'),
            'gender': data.get('gender'),
            'email': data.get('email'),
            'external_email': data.get('external_email'),

            })

            return Response(
                json.dumps({'message':'Teacher successfully created!','status':200}),
                content_type="application/json",
                status=200)

        except ValidationError as e:
            return Response(
                json.dumps({'message': str(e), 'status': 400}),
                content_type='application/json;charset=utf-8',
                status=400)

        except Exception as e:
            return Response(
                json.dumps({'message': str(e), 'status': 500}),
                content_type='application/json;charset=utf-8',
                status=500)