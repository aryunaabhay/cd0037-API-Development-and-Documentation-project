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
        database_path = test_config.get("SQLALCHEMY_DATABASE_URI")
        setup_db(app, database_path=database_path)

    # Set up CORS to allow '*' for origins
    CORS(app, resources={r"/*": {"origins": "*"}})

    with app.app_context():
        db.create_all()

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    @app.route("/categories")
    def get_categories():
        try:
            categories = Category.query.all()
            return jsonify(
                {
                    "success": True,
                    "categories": {
                        category.id: category.type for category in categories
                    },
                }
            )
        except:
            abort(500)

    @app.route("/questions", methods=["GET"])
    def get_questions():
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        try:
            query = Question.query
            total_questions = query.count()

            # If the page is out of range, return an empty list
            if page > (total_questions / per_page if total_questions > per_page else 1):
                return jsonify({"success": True, "questions": [], "total_questions": 0})

            questions = query.paginate(page=page, per_page=per_page, count=False)
            print(questions)
            print(questions.items)
            print(questions.total)
            categories = Category.query.all()

            return jsonify(
                {
                    "success": True,
                    "questions": [question.format() for question in questions],
                    "total_questions": total_questions,
                    "categories": {
                        category.id: category.type for category in categories
                    },
                    "current_category": "Science",
                }
            )
        except ApiError:
            raise
        except Exception as e:
            abort(500)

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            if question is None:
                raise ApiError(status_code=404, error={"message": "Not Found"})
            question.delete()
            return jsonify({"success": True, "deleted": question_id})
        except ApiError:
            raise
        except Exception as e:
            abort(500)

    @app.route("/questions", methods=["POST"])
    def create_question():
        data = request.get_json()
        if data is None:
            raise ApiError({"message": "Bad Request"}, 400)

        question = data.get("question")
        answer = data.get("answer")
        category_id = data.get("category")
        difficulty = data.get("difficulty")
        print(category_id)

        if (
            question is None
            or answer is None
            or category_id is None
            or difficulty is None
        ):
            raise ApiError({"message": "Bad Request"}, 400)

        category = Category.query.filter(Category.id == category_id).one_or_none()
        if category is None:
            raise ApiError({"message": "Unprocessable Entity"}, 422)

        try:
            question = Question(
                question=question,
                answer=answer,
                category=category_id,
                difficulty=difficulty,
            )
            question.insert()
            return jsonify({"success": True, "created": question.id})
        except ApiError:
            raise
        except Exception as e:
            abort(500)

    @app.route("/questions/search", methods=["POST"])
    def questions_search():
        data = request.get_json()
        search_term = data.get("searchTerm")
        if search_term is None:
            abort(400)

        try:
            questions = Question.query.filter(
                Question.question.ilike(f"%{search_term}%")
            ).all()
            return jsonify(
                {
                    "success": True,
                    "questions": [question.format() for question in questions],
                    "total_questions": len(questions),
                }
            )
        except:
            abort(500)

    @app.route("/categories/<string:category_id>/questions", methods=["GET"])
    def get_questions_by_category(category_id):
        try:
            category = Category.query.filter(Category.id == category_id).one_or_none()
            if category is None:
                raise ApiError({"message": "Not Found"}, 404)

            questions = Question.query.filter(Question.category == category_id).all()
            return jsonify(
                {
                    "success": True,
                    "questions": [question.format() for question in questions],
                }
            )
        except ApiError:
            raise
        except Exception as e:
            print(e)
            abort(500)

    @app.route("/quizzes", methods=["POST"])
    def get_quizz_questions():
        data = request.get_json()
        request_category = data.get("quiz_category")
        category_id = request_category.get("id")
        previous_questions = data.get("previous_questions")

        if category_id is None:
            raise ApiError({"message": "Not Found"}, 404)

        if request_category.get("type") != "ALL":
            category = Category.query.filter(Category.id == category_id).one_or_none()
            if category is None:
                raise ApiError({"message": "Not Found"}, 404)

        try:
            filters = [Question.id.not_in(previous_questions)]
            if request_category.get("type") == "ALL":
                filters.append(Question.category != category_id)

            questions = Question.query.filter(*filters).all()

            if len(questions) == 0:
                return jsonify({"success": True, "question": None})

            return jsonify(
                {
                    "success": True,
                    "question": questions[
                        random.randint(0, len(questions) - 1)
                    ].format(),
                }
            )
        except Exception as e:
            print(e)
            abort(500)

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
