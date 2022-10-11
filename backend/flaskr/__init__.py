import os
import random
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def get_page_item_offset(request):
    page_number = request.args.get('page', 1, type=int)
    item_start_index = (page_number - 1) * QUESTIONS_PER_PAGE
    return item_start_index

def get_categories():
    categories = {}
    for category in Category.query.all():
        categories.update(category.format())
    return categories

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r'/*': {'origins': '*'}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorisation')
        response.headers.add('Access-Contrl-Allow-Methods', 'DELETE, PATCH, GET, OPTIONS, POST')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories/')
    def categories():
        categories = get_categories()
        
        if categories:
            return jsonify({
                'success': True, 
                'categories': categories
            })
        else:
            abort(404)


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
    @app.route('/questions/')
    def questions():
        start = get_page_item_offset(request)
        end = start + QUESTIONS_PER_PAGE
        categories = get_categories()
        questions = Question.query.all()
        questions_count = Question.query.count()
        # check if question exist for the requested page
        if questions_count > 0 and questions_count >= start:
            questions = questions[start:end]
            return jsonify({
                'success': True,
                'questions': [question.format() for question in questions],
                'total_questions': questions_count,
                'categories': categories,
                'current_category': None,
            })
        else:
            abort(404)


    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        
        question = (Question.query
            .filter(Question.id==id)
            .one_or_none())
        
        if question is None:
            abort(404)
        
        try:
            question.delete() 
        except:
            abort(422)
        
        return jsonify({
            'success': True,
        })

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
    def save_question():
        
        question_fields = ['question', 'answer', 'difficulty', 'category']
        new_question = {}
        
        # abort and return bad request 400 on invalid payload
        for key in question_fields:
            new_question[key] = request.get_json().get(key, None)
            if new_question[key] == None:
                abort(400)
        
        try:
            question = Question(**new_question)
            question.insert()

            return jsonify({
                'success': True
            })
        except:
            abort(422)



    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/search', methods=['POST'])
    def search_questions():
        
        search_term = request.get_json().get('searchTerm', None)
        if search_term == None:
            abort(400)
        questions = Question.query.filter(
            Question.question.ilike('%{}%'.format(search_term)))
        
        questions_count = questions.count()

        if questions_count == 0:
            abort(404)

        questions = [question.format() for question in questions.all()]
        
        return jsonify({
            'success': True,
            'questions': questions,
            'total_questions': questions_count,
            'current_category': None,
        })



    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route('/categories/<int:id>/questions')
    def get_questions_by_category(id):
        current_category = Category.query.filter(Category.id==id).one_or_none()
        questions = Question.query.filter(Question.category==id)
        questions_count = questions.count()

        if questions_count == 0 and current_category is None:
            abort(404)
        
        return jsonify({
            'success': True,
            'questions': [question.format() for question in questions.all()],
            'total_questions': questions_count,
            'current_category': current_category.type
        })

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
    def next_quiz_question():
       
        previous_questions = request.get_json().get("previous_questions", [])
        quiz_category = request.get_json().get("quiz_category", None)
        
        # get question by category
        if quiz_category is None:
            abort(400)

        # find new question not on the previous list
        question = (Question.query
            .filter(~Question.id.in_(previous_questions))
            .filter(Question.category==quiz_category['id'])
            .limit(1)
            .one_or_none())

        if question is None:
            abort(404)
        
        return jsonify({'success': True, 'question': question.format()})
        
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(400)
    def invalid_request(error):
        return jsonify({
            "success": False, 
            "error": 400,
            "message": "Invalid request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "Requested resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessed_request(error):
        return jsonify({
            "success": False, 
            "error": 422,
            "message": "Sorry, could not process your request"
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False, 
            "error": 500,
            "message": "Server error"
        }), 500

    return app