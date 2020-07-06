from pydblite.sqlite import Database, Table

class DBConnect(object):
    """[configure pydblite db connection]
    
    Arguments:
        object {[Object]} -- [description]
    """

    db = Database('grading_app_db', check_same_thread=False)

    students_table = Table("Students", db)
    assignments_table = Table("Assignments", db)
    questions_table = Table("Questions", db)
    grades_table = Table("Grades", db)
    assignments_students_table = Table("Assignments_Students", db)

    db.conn.text_factory = str

    def __init__(self):
        self.students_table.create(
            ('id', 'TEXT'),
            ('name', 'TEXT'),
             mode="open" )

        self.assignments_table.create(
            ('id', 'TEXT'),
            ('name', 'TEXT'),
            ('grade_details_01', 'TEXT'),
            ('grade_details_02', 'TEXT'),
            ('grade_details_03', 'TEXT'),
            ('grade_details_04', 'TEXT'),
            ('pass_mark', 'INTEGER'),
             mode="open" )

        self.questions_table.create(
            ('id', 'TEXT'),
            ('assignmentId', 'TEXT'),
            ('question', 'TEXT'),
            ('answer_01', 'TEXT'),
            ('answer_02', 'TEXT'),
            ('answer_03', 'TEXT'),
            ('answer_04', 'TEXT'),
            ('correct_answer', 'TEXT'),
            ('marks', 'INTEGER'),
             mode="open" )

        self.grades_table.create(
            ('id', 'TEXT'),
            ('studentId', 'TEXT'),
            ('assignmentId', 'TEXT'),
            ('questionId', 'TEXT'),
            ('timeSpent', 'REAL'),
            ('answer', 'TEXT'),
            ('marks', 'INTEGER'),
             mode="open" )

        self.assignments_students_table.create(
            ('id', 'TEXT'),
            ('assignmentId', 'TEXT'),
            ('studentId', 'TEXT'),
             mode="open" )

