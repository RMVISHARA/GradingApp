import uuid

class DBService:

    def __init__(self, db_conn):
        self.__db_conn = db_conn


    def add_student(self, name):
        """[Add student details to the db]

        Args:
            name ([string]): [name of the student]

        Returns:
            [string]: [added student's id]
        """
        check_student = self.check_student(name)
        if(len(check_student) == 0):
            student_id = str(uuid.uuid4())
            self.__db_conn.students_table.open()
            self.__db_conn.students_table.insert(
                id = student_id,
                name = name
            )
            self.__db_conn.students_table.commit()
            return student_id
        else:
            return check_student[0]['id']

    def check_student(self, name):
        """[Check whether student is already in the system or not]

        Args:
            name ([string]): [name of the student]

        Returns:
            [object]: [details of the student]
        """        
        self.__db_conn.students_table.open()
        rec = self.__db_conn.students_table(name = name)
        return rec

    def get_all_assignments(self):
        """[Get all assignments]

        Returns:
            [array]: [all available assignments]
        """        
        assignments = self.__db_conn.assignments_table()
        return assignments

    def get_all_questions(self, assignment_id):
        """[Get all questions which are related to the assignment]

        Args:
            assignment_id ([string]): [id of the selected assignment]

        Returns:
            [array]: [all question related data]
        """        
        questions = self.__db_conn.questions_table(assignmentId = assignment_id)
        return questions

    def add_answers(self, answer_obj, question_id):
        """[Add stuents answers]

        Args:
            answer_obj ([object]): [all question and answer related data]
            question_id ([string]): [unique identifier of the question]
        """        
        self.__db_conn.grades_table.open()
        self.__db_conn.grades_table.insert(
            id = str(uuid.uuid4()),
            studentId = answer_obj['studentId'],
            assignmentId = answer_obj['assignmentId'],
            questionId = question_id,
            timeSpent = 0,
            answer = answer_obj['answer'],
            marks = answer_obj['marks']
        )
        self.__db_conn.grades_table.commit()
    
    def update_time(self, spent_time_obj):
        """[Update spent time forr a question]

        Args:
            spent_time_obj ([object]): [details of the question]
        """        
        results = [r for r in self.__db_conn.grades_table if r['assignmentId'] == spent_time_obj['assignmentId'] and r['studentId'] == spent_time_obj['studentId']]
        for i in range(len(results)):
            if(results[i]['questionId'] == spent_time_obj['timeQuestions'][i]['questionId']):
                self.__db_conn.grades_table.update(results[i], timeSpent = spent_time_obj['timeQuestions'][i]['timeSpent'])
        self.__db_conn.grades_table.commit()


    def assign_student_to_assignment(self, student_id, assignment_id):
        """[Assign an assignment to student]

        Args:
            student_id ([string]): [unique identifier of the student]
            assignment_id ([string]): [unique identifier of the assignment]
        """        
        self.__db_conn.assignments_students_table.open()
        self.__db_conn.assignments_students_table.insert(
            id = str(uuid.uuid4()),
            studentId = student_id,
            assignmentId = assignment_id,
        )
        self.__db_conn.assignments_students_table.commit()

    def get_student_assignments(self, student_id):
        """[Get assignments which are related to the student]

        Args:
            student_id ([string]): [unique identifier of the student]

        Returns:
            [array]: [assignments which are related to particular student]
        """
        all_courses = []
        student_courses = self.__db_conn.assignments_students_table(studentId = student_id)
        # print(student_courses)
        for c in student_courses:
            courses = self.__db_conn.assignments_table(id = c['assignmentId'])
            for course in courses:
                all_courses.append(course)
        return all_courses



    def calculate_marks(self, student_id, assignment_id):
        """[Calculate total marks for a specific module]

        Args:
            student_id ([string]): [unique identifier of the student]
            assignment_id ([string]): [unique identifier of the assignment]

        Returns:
            [integer]: [total marks of the assignment]
        """        
        total_marks = 0
        for rec in self.__db_conn.grades_table(studentId = student_id):
            if rec['assignmentId'] == assignment_id:
                total_marks = total_marks + rec['marks']
        # 
        return total_marks

    
    def get_student_grades(self):
        """[Get all students grades]

        Returns:
            [array]: [students grade details]
        """        
        all_students = self.__db_conn.students_table()
        student_grades = []
        for student in all_students:
            student_grade_obj = {
                "id" : student['id'],
                "name" : student['name'],
                "assignments" : []
            }
            assignments = self.get_student_assignments(student['id'])
            for a in assignments:
                marks = self.calculate_marks(student['id'], a['id'])
                assignment_obj = {
                    "id" : a['id'],
                    "name" : a['name'],
                    "marks" : marks
                }
                student_grade_obj['assignments'].append(assignment_obj)
            student_grades.append(student_grade_obj)
        return student_grades

                
    def get_student_papers(self, student_id, assignment_id):
        """[Get all questions which are related to the assignment]

        Args:
            student_id ([type]): [unique identifier of the student]
            assignment_id ([type]): [unique identifier of the assignment]

        Returns:
            [array]: [all thw questions which are related to the assignment]
        """        
        questions = self.get_all_questions(assignment_id)
        all_questions = []
        for q in questions:
            answer = self.get_student_answer(student_id, q['id'])
            question = {
                "id" : q['id'],
                "question" : q["question"],
                "answer_01" : q["answer_01"],
                "answer_02" : q["answer_02"],
                "answer_03" : q["answer_03"],
                "answer_04" : q["answer_04"],
                "correct_answer" : q["correct_answer"],
                "answer" : answer 
            }
            all_questions.append(question)
        return all_questions


    def get_student_answer(self, student_id, question_id):
        """[Get student's answer for a question]

        Args:
            student_id ([string]): [unique identifier of the student]
            question_id ([string]): [unique identifier of the question]

        Returns:
            [integer]: [student's answer]
        """        
        result = [r for r in self.__db_conn.grades_table if r['questionId'] == question_id and r['studentId'] == student_id]
        return result[0]['answer']

    def calculate_average_time(self, question_id):
        """[Calculate average time for a single question]

        Args:
            question_id ([string]): [unique identifier of the question]

        Returns:
            [float]: [average time for a single question]
        """        
        questions = self.__db_conn.grades_table(questionId = question_id)
        total_time = 0
        print(len(questions))
        for q in questions:
            total_time = total_time + q['timeSpent']
        average_time = total_time / len(questions)
        return average_time

    def mark_answers(self, question_id):
        """[Get correct and incorrect answers for a single question]

        Args:
            question_id ([string]): [unique identifier of the question]

        Returns:
            [object]: [correct and incorrect answers count]
        """        
        questions = self.__db_conn.grades_table(questionId = question_id)
        correct = 0
        incorrect = 0
        for q in questions:
            if q['marks'] > 0:
                correct = correct + 1
            else:
                incorrect = incorrect + 1
        return {
            "correct" : correct,
            "incorrect" : incorrect
        }

    def get_question_statistics(self):
        """[Get statistics of questions]

        Returns:
            [array]: [all assignment with answers]
        """        
        assignments = self.get_all_assignments()
        assignment_stats = []
        for a in assignments:
            assignment_obj = {
                "id" : a['id'],
                "name" : a['name'],
                "questions" : []
            }
            questions = self.get_all_questions(a['id'])
            for q in questions:
                average_time = self.calculate_average_time(q['id'])
                answer_count = self.mark_answers(q['id'])
                question = {
                    "id" : q['id'],
                    "question" : q["question"],
                    "average_time" : average_time,
                    "correct" : answer_count['correct'],
                    "incorrect" : answer_count['incorrect']
                }
                assignment_obj['questions'].append(question)
            assignment_stats.append(assignment_obj)
        return assignment_stats