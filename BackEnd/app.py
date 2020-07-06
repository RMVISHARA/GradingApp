from datetime import datetime
from flask import Flask,jsonify
from flask_restplus import Api, Resource, fields
from flask_cors import CORS, cross_origin
from infrastructure.db_connect import DBConnect
from services.db_service import DBService

db_conn = DBConnect()
db_service = DBService(db_conn)

app = Flask(__name__)
CORS(app)

api = Api(app, version='1.0', title='Grading App',
    description='',
)

add_student_api = api.namespace('addStudent', description='Assign student to the assignment')
question_api = api.namespace('question', description='Question Management')

# exposed apis
student_api = api.namespace('student', description='Studet View')
teacher_api = api.namespace('teacher', description='Teacher View')

student_model = api.model('AssignStudent',{
    'name': fields.String(required=True, description='Name of the student'),
    'assignment_id': fields.String(required=True, description='Id of the assignment')
})

question_model = api.model('AnswerQuestion',{
    'studentId': fields.String(required=True, description='Id of the student'),
    'assignmentId': fields.String(required=True, description='Id of the assignment'),
    'answer': fields.String(required=True, description='Answer of the student'),
    'marks': fields.Integer(required=True, description='Marks of the question'),
})

time_spent_model = api.model('AssignStudent',{
    'questionId': fields.String(required=True, description='Id of the question'),
    'timeSpent': fields.Float(required=True, description='Spent Time for a question')
})


question_details_model = api.model('SpenTime',{
    'studentId': fields.String(required=True, description='Id of the student'),
    'assignmentId': fields.String(required=True, description='Id of the assignment'),
    'timeQuestions': fields.List(fields.Nested(time_spent_model)),
})





@add_student_api.route('/')
class AssignStudentToAssignment(Resource):
    """[assign student to assignment api]

    Arguments:
        Resource {[Object]} -- [package of the flask_restplus]
    """

    @add_student_api.doc('assign_student')
    @add_student_api.expect(student_model)
    def post(self):
        '''Assign student to an assignment'''
        try:
            student_id = db_service.add_student(api.payload['name'])
            db_service.assign_student_to_assignment(student_id, api.payload['assignment_id'])
            return jsonify(student_id)
        except Exception as e:
            return jsonify(str(e))


@question_api.route('/answer/<string:question_id>')
class AnswerQuestions(Resource):
    """[answer questions api]

    Arguments:
        Resource {[Object]} -- [package of the flask_restplus]
    """

    @question_api.doc('answer_question')
    @question_api.expect(question_model)
    def post(self, question_id):
        '''Answer questions which are related to an assignment'''
        try:
            db_service.add_answers(api.payload, question_id)
            return jsonify("ok")
        except Exception as e:
            return jsonify(str(e))

@question_api.route('/timeSpent')
class UpdateTime(Resource):
    """[update time api]

    Arguments:
        Resource {[Object]} -- [package of the flask_restplus]
    """

    @question_api.doc('time_spent_question')
    @question_api.expect(question_details_model)
    def post(self):
        '''Update spent time according to the question'''
        try:
            db_service.update_time(api.payload)
            return jsonify("ok")
        except Exception as e:
            return jsonify(str(e))

@question_api.route('/assignment/<string:assignment_id>')
class GetQuestions(Resource):
    """[get questions api]

    Arguments:
        Resource {[Object]} -- [package of the flask_restplus]
    """

    @question_api.doc('get_question')
    def get(self, assignment_id):
        '''Get all the questions which is related to the assignment'''
        try:
            questions = db_service.get_all_questions(assignment_id)
            return jsonify(questions)
        except Exception as e:
            return jsonify(str(e))


@student_api.route('/results')
class GetResults(Resource):
    """[get student results api]

    Arguments:
        Resource {[Object]} -- [package of the flask_restplus]
    """

    @student_api.doc('get_results')
    def get(self):
        '''Get results of the all students'''
        try:
            results = db_service.get_student_grades()
            return jsonify(results)
        except Exception as e:
            return jsonify(str(e))


@student_api.route('/review/<string:student_id>/<string:assignment_id>')
class ReviewPaper(Resource):
    """[review results api]

    Arguments:
        Resource {[Object]} -- [package of the flask_restplus]
    """

    @student_api.doc('review_paper')
    def get(self, student_id, assignment_id):
        '''Review results of specific assignment'''
        try:
            results = db_service.get_student_papers(student_id, assignment_id)
            return jsonify(results)
        except Exception as e:
            return jsonify(str(e))

@teacher_api.route('/details')
class AssignmentDetails(Resource):
    """[assignment details api]

    Arguments:
        Resource {[Object]} -- [package of the flask_restplus]
    """

    @teacher_api.doc('get_assignment_details')
    def get(self):
        '''Get assignment details'''
        try:
            assignments = db_service.get_all_assignments()
            return jsonify(assignments)
        except Exception as e:
            return jsonify(str(e))


@teacher_api.route('/statistics')
class QuestionStatistics(Resource):
    """[question statistics api]

    Arguments:
        Resource {[Object]} -- [package of the flask_restplus]
    """

    @teacher_api.doc('get_statistics')
    def get(self):
        '''GHet statistics of the questions'''
        try:
            results = db_service.get_question_statistics()
            return jsonify(results)
        except Exception as e:
            return jsonify(str(e))


if __name__ == '__main__':
    app.run(debug=True)