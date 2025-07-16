import os
import unittest

from werkzeug.wrappers import response

from flaskr import create_app
from models import db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = "trivia_test"
        self.database_user = "postgres"
        self.database_password = "password"
        self.database_host = "localhost:5432"
        self.database_path = f"postgresql://{self.database_user}:{self.database_password}@{self.database_host}/{self.database_name}"

        # Create app with the test configuration
        self.app = create_app(
            {
                "SQLALCHEMY_DATABASE_URI": self.database_path,
                "SQLALCHEMY_TRACK_MODIFICATIONS": False,
                "TESTING": True,
            }
        )
        self.client = self.app.test_client()

        # Bind the app to the current context and create all tables
        with self.app.app_context():
            db.create_all()
            self.create_test_data()

    def tearDown(self):
        """Executed after each test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def create_test_data(self):
        """Create test data for the database"""
        category1 = Category(type="Science")
        category2 = Category(type="History")
        category1.insert()
        category2.insert()

        # Create test questions
        question1 = Question(
            question="What is the capital of France?",
            answer="Paris",
            category=1,
            difficulty=1,
        )
        question2 = Question(
            question="What is 2+2?", answer="4", category=1, difficulty=1
        )
        question3 = Question(
            question="What is the capital of Germany?",
            answer="Berlin",
            category=2,
            difficulty=1,
        )
        question1.insert()
        question2.insert()

    def test_get_categories(self):
        res = self.client.get("/categories")
        response_data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(response_data["success"], True)
        self.assertTrue(response_data["categories"])

    def test_get_questions(self):
        res = self.client.get("/questions")
        response_data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(response_data["success"], True)
        self.assertTrue(response_data["questions"])
        self.assertTrue(response_data["total_questions"])

    def test_get_questions_with_page_and_per_page(self):
        res = self.client.get("/questions?page=1&per_page=10")
        response_data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(response_data["success"], True)
        self.assertTrue(response_data["questions"])
        self.assertTrue(response_data["total_questions"])
        self.assertEqual(len(response_data["questions"]), 2)

    def test_pagination_out_of_range(self):
        res = self.client.get("/questions?page=1000&per_page=10")
        response_data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(response_data["questions"], [])

    def test_create_question(self):
        new_question = {
            "question": "What is the capital of France?",
            "answer": "Paris",
            "category": "1",
            "difficulty": 1,
        }
        res = self.client.post("/questions", json=new_question)
        response_data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(response_data["success"], True)
        self.assertTrue(response_data["created"])

    def test_question_creation_non_existing_category(self):
        new_question = {
            "question": "What is the capital of France?",
            "answer": "Paris",
            "category": "100",
            "difficulty": 1,
        }
        res = self.client.post("/questions", json=new_question)
        response_data = res.get_json()
        self.assertEqual(res.status_code, 422)
        self.assertEqual(response_data["message"], "Unprocessable Entity")

    def test_delete_question(self):
        res = self.client.delete("/questions/1")
        response_data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(response_data["success"], True)
        self.assertEqual(response_data["deleted"], 1)

    def test_delete_non_existing_question(self):
        res = self.client.delete("/questions/100")
        response_data = res.get_json()
        self.assertEqual(res.status_code, 404)
        self.assertEqual(response_data["message"], "Not Found")

    def test_search_questions(self):
        res = self.client.post("/questions/search", json={"searchTerm": "france"})
        response_data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(response_data["success"], True)
        self.assertEqual(len(response_data["questions"]), 1)

    def test_search_questions_no_results(self):
        res = self.client.post("/questions/search", json={"searchTerm": "no results"})
        response_data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(response_data["success"], True)
        self.assertEqual(len(response_data["questions"]), 0)

    def test_get_questions_by_category(self):
        res = self.client.get("/categories/1/questions")
        response_data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(response_data["success"], True)
        questions = response_data["questions"]
        self.assertEqual(len(questions), 2)

    def test_get_questions_by_category_non_existing_category(self):
        res = self.client.get("/categories/100/questions")
        response_data = res.get_json()
        self.assertEqual(res.status_code, 404)
        self.assertEqual(response_data["message"], "Not Found")

    def test_get_quizz_questions(self):
        res = self.client.post(
            "/quizzes",
            json={
                "quiz_category": {"id": 1},
                "category_id": 1,
                "previous_questions": [],
            },
        )
        response_data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(response_data["success"], True)
        self.assertTrue(response_data["question"])

    def test_get_quizz_questions_non_existing_category(self):
        res = self.client.post(
            "/quizzes",
            json={
                "quiz_category": {"id": 100},
                "category_id": 100,
                "previous_questions": [],
            },
        )
        response_data = res.get_json()
        self.assertEqual(res.status_code, 404)
        self.assertEqual(response_data["message"], "Not Found")

    def test_get_quizz_questions_no_questions(self):
        res = self.client.post(
            "/quizzes",
            json={
                "quiz_category": {"id": 1},
                "category_id": 1,
                "previous_questions": [1, 2],
            },
        )
        response_data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(response_data["success"], True)
        self.assertEqual(response_data["question"], None)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
