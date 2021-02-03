import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        # self.database_name = "trivia_test"
        # self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        self.database_path = "postgresql://postgres:0000@localhost:5432/TriviaDB"
        setup_db(self.app, self.database_path)

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
        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.Status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_delete_questions(self):
        res = self.client().delete('/questions/5')
        data = json.loads(res.data)

        self.assertEqual(res.Status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_create_questions(self):
        res = self.client().post('/add', json=Question(
            "What is the name of red planet?", "Mars", 1, 1))
        data = json.loads(res.data)

        self.assertEqual(res.Status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_search_questions(self):
        res = self.client().post('/search-questions', json="ball")
        data = json.loads(res.data)

        self.assertEqual(res.Status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_search_questions_by_category(self):
        res = self.client().get('/categories/3/questions')
        data = json.loads(res.data)

        self.assertEqual(res.Status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_play_quiz(self):
        res = self.client().post('/play',
                                 json={'previous_questions': [10], 'quiz_category': {'type': 'Sports', 'id': '6'}})
        data = json.loads(res.data)

        self.assertEqual(res.Status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
