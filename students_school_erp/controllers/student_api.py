from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request, Response
import json


class StudentAPI(http.Controller):

    @http.route(['/api/student/<student_id>'], type='http', auth='user', methods=['GET'], csrf=False)
    def get_student_info(self, student_id):
        """
        API to take information with student id
        """
        student = request.env['students.students'].browse(int(student_id))

        if not student.exists():
            return Response(
                json.dumps({'success': False, 'message': 'student not found'}),
                content_type='application/json;charset=utf-8', status=404)
        data = {
            'success': True,
            'student_id': student.id,
            'sequence': student.sequence,
            'name': student.name,
            'surname': student.surname,
            'father_name': student.father_name,
            'mother_name': student.mother_name,
            'external_email': student.external_email,
            'gender': student.gender,
            'dob': str(student.dob) if student.dob else None,
            'blood_type': student.blood_type,
            'year': student.year,
            'faculty': student.faculty,
        }
        return Response(
            json.dumps(data),
            content_type='application/json;charset=utf-8', status=200)

    @http.route(['/api/student/list_students'], type='http', auth='user', methods=['GET'], csrf=False)
    def get_students(self):
        """
        List all the students that exist
        """
        students = request.env['students.students'].search([])

        data = []
        for rec in students:
            data.append({
                'id': rec.id,
                'sequence': rec.sequence,
                'name': rec.name,
                'surname': rec.surname,
                'email': rec.email,
                'state': rec.state,
                'classroom': rec.classroom_id.name if rec.classroom_id else None,
                'year': rec.year,
                'faculty': rec.faculty,
            })

        return Response(
            json.dumps(data),
            content_type='application/json',
            status=200
        )

    @http.route('/api/student/create_student', type='http', auth='user', methods=['POST'], csrf=False)
    def create_student(self):

        data = request.jsonrequest
        try:
            student = request.env['students.students'].create({
                'name': data.get('name'),
                'surname': data.get('surname'),
                'email': data.get('email'),
                'state': data.get('state'),
                'father_name': data.get('father_name'),
                'mother_name': data.get('mother_name'),
                'external_email': data.get('external_email'),
                'gender': data.get('gender'),
                'dob': data.get('dob'),
                'blood_type': data.get('blood_type'),
                'year': data.get('year'),
                'faculty': data.get('faculty'),
                'semester': data.get('semester'),

            })
            return Response(
            json.dumps({
                'message': 'Student created!',
                'status': 200, }),
                content_type='application/json;charset=utf-8', status=200)

        except ValidationError as e:
            return Response(
                json.dumps({'message':str(e),'status': 400}),
                content_type='application/json;charset=utf-8', status=400)

        except Exception as e:
            return Response(
                json.dumps({'message':str(e),'status': 500}),
                content_type='application/json;charset=utf-8', status=500
            )