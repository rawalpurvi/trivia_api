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
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}@{}/{}".format('purvi', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        # Create New Question
        self.new_question = {
            'question': 'What is Earth-s largest continent?',
            'answer': 'Asia',
            'category': 3,
            'difficulty': 4,
            'rating': 5
        }    
    
        # Create valid quiz category
        self.quiz_category_valid = {
            'quiz_category': {
                'id': 1,
                'type': 'Science'
            }      
        }    
        
        # Create false quiz category
        self.quiz_category_invalid = {
            'quiz_category': {
                'id': 10,
                'type': 'Math'
            }
        }    

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    # Run test to check Paginate Questions and Error occures

    def test_get_paginate_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('questions?page=1000')    
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Run test to delete Question and Error occures

    def test_delete_question(self):
        res = self.client().delete('questions/33')
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == 33).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 33)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(question, None)

    def test_400_if_question_does_not_exit(self):
        res = self.client().delete('/questions/1000') 
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')        

    # Run test to delete Question and Error occures

    def test_add_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['questions']))       

    def test_405_if_question_addition_not_allowed(self):
        res = self.client().post('/questions/45', json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    # Test for search questions are with or without list    

    def test_get_question_search_with_results(self):
        res = self.client().post('/search', json={'searchTerm':'what'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']),1)

    def test_get_question_search_without_results(self):
        res = self.client().post('/search', json={'searchTerm':'Harry Potter'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'],0)
        self.assertEqual(len(data['questions']),0)    
    
    # Test for get questions for specific category

    def test_get_question_for_specific_categories(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']),1)

    def test_404_no_specific_category(self):
        res = self.client().get('/categories/10/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Test to play trivia quiz

    def test_to_play_trivia_quiz(self):
        res = self.client().post('/quizzes', json=self.quiz_category_valid)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['question']),1)

    def test_404_no_question_found(self):
        res = self.client().post('/quizzes', json=self.quiz_category_invalid)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()