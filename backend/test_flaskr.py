import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

database_host = os.getenv('DB_HOST', 'localhost:5432')
database_user = os.getenv('DB_USER', 'postgres')
database_password = os.getenv('DB_PASSWORD', '1234')
database_name = os.getenv('DB_NAME', 'trivia_test')
database_path = 'postgresql://{}:{}@{}/{}'.format(
    database_user, 
    database_password, 
    database_host, 
    database_name)

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app, database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_questions(self):
        res = self.client().get("/questions/")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_404_for_invalid_page_request(self):
        res = self.client().get("/questions/?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Requested resource not found")

    def test_for_create_question(self):
        res = self.client().post(
            '/questions', 
            json={'question': "question", 'answer': "answer", 'difficulty': 1, 'category': 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        
        # remove question
        Question.query.filter(
            Question.question=='question',
            Question.answer=='answer'
        ).delete()

    def test_400_for_failed_question_creation(self):
        res = self.client().post(
            '/questions', 
            json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Invalid request")
    
    def test_delete_question(self):
        new_question = {'question': "question", 'answer': "answer", 'difficulty': 1, 'category': 1}
        question = Question(**new_question)
        question.insert()
        res = self.client().delete('/questions/{}'.format(question.id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
    
    def test_404_if_question_does_not_exist(self):
        res = self.client().delete('/questions/{}'.format(1000))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Requested resource not found")

    def test_for_quizzes(self):
        quiz_category = {"id": 3, "type":"Geography"}
        res = self.client().post(
            "/quizzes", 
            json={"previous_questions": [], "quiz_category": quiz_category})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['question'])
    
    def test_400_for_invalid_quiz_request(self):
        res = self.client().post(
            "/quizzes",
            json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_200_for_category_list(self):
        res = self.client().get("/categories/")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data['categories'])

    def test_questions_by_category(self):
        res = self.client().get("/categories/{}/questions".format(1))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_404_if_category_does_not_exist(self):
        res = self.client().get("/categories/{}/questions".format(6000))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])

    def test_for_search(self):
        res = self.client().post(
            "/search", 
            json={'searchTerm': 'city'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
    
    def test_404_if_search_term_not_found(self):
        res = self.client().post(
            "/questions/search", 
            json={'searchTerm': '436547s'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()