from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path)

    # Set up CORS to allow '*' for origins
    CORS(app, resources={r"/*": {"origins": "*"}})

    with app.app_context():
        db.create_all()

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response


    @app.route('/categories')
    def get_categories():
        try:
            categories = Category.query.all()
            return jsonify({
                'success': True,
                'categories': {category.id: category.type for category in categories}
            })
        except:
            abort(500)
        
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions', methods=['GET'])
    def get_questions():
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        try:
            query = Question.query
            total_questions = query.count()
            questions = query.paginate(page=page, per_page=per_page, count=False)
            categories = Category.query.all()

            return jsonify({
                'success': True,
                'questions': [question.format() for question in questions],
                'total_questions': total_questions,
                'categories': {category.id: category.type for category in categories},
                'current_category': 'Science'
            })
        except Exception as e:
            print(e)
            abort(500)
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.
    
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            if question is None:
                abort(404)
            try:
                question.delete()
            except:
                abort(500)
            
            return jsonify({
                'success': True,
                'deleted': question_id
            })
        except:
            abort(500)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        data = request.get_json()
        if data is None:
            abort(400)

        question = data.get('question')
        answer = data.get('answer')
        category = data.get('category')
        difficulty = data.get('difficulty')
        if question is None or answer is None or category is None or difficulty is None:
            abort(400)
        try:
            question = Question(question=question, answer=answer, category=category, difficulty=difficulty)
            question.insert() 
            return jsonify({
                'success': True,
                'created': question.id
            })
        except Exception as e:
            abort(500)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route('/questions/search', methods=['POST'])
    def questions_search():
        data = request.get_json()
        search_term = data.get('searchTerm')
        if search_term is None:
            abort(400)

        try:
            questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
            return jsonify({
                'success': True,
                'questions': [question.format() for question in questions],
                'total_questions': len(questions)
            })
        except:
            abort(500)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        try:
            questions = Question.query.filter(Question.category == category_id).all()
            return jsonify({
                'success': True,
                'questions': [question.format() for question in questions]
            })
        except:
            abort(500)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def get_quizz_questions():
        data = request.get_json()
        category = data.get('quiz_category')
        category_id = category.get('id')
        previous_questions = data.get('previous_questions')
        if category_id is None:
            abort(400)
        try:
            questions = Question.query.filter(Question.category == category_id, Question.id.not_in(previous_questions)).all()
            return jsonify({
                'success': True,
                'question': questions[random.randint(0, len(questions) - 1)].format()
            })
        except Exception as e:
            print(e)
            abort(500)
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(ApiError)
    def handle_api_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    return app


class ApiError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code
