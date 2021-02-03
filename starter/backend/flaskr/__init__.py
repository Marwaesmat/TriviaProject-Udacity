import os
from flask import Flask, request, abort, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import cast, Integer, func
from flask_cors import CORS
import random

from models import db, setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
  # create and configure the app
    app = Flask(__name__)
    setup_db(app)

  # ***DONE***@TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs

    CORS(app, resources={r"/api/*": {"origins": "*"}})
    # CORS(app)

  # ***DONE***@TODO: Use the after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')  # Specify which hearders allowed to use, which are content-type and authorization
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, DELETE, OPTIONS')   # Specify allowed methods to use
        return response

    @app.route('/')
    def index():
        componentDidMount()
        return jsonify({'success': True})

  # ***DONE***@TODO:
  # Create an endpoint to handle GET requests
  # for all available categories.
    @ app.route('/categories', methods=['GET'])
    def componentDidMount():
        data_cat = {}
        for cat in Category.query.all():
            data_cat[cat.id] = cat.type
        return jsonify({'success': True, 'categories': data_cat})

  # ***DONE***@TODO:
  # Create an endpoint to handle GET requests for questions,
  # including pagination (every 10 questions).
  # This endpoint should return a list of questions,
  # number of total questions, current category, categories.
    @ app.route('/questions', methods=['GET'])
    def getQuestions():
        page = request.args.get('page', 1, type=int)
        ques_dic = {}
        questions = {}
        ques_dic['questions'] = []
        data_cat = {}
        data_ques = db.session.query(Question, Category).join(
            Category).filter(Question.category == Category.id)
        ques_cats = data_ques.paginate(page, QUESTIONS_PER_PAGE).items
        for q in ques_cats:
            questions['id'] = q.Question.id
            questions['question'] = q.Question.question
            questions['answer'] = q.Question.answer
            questions['difficulty'] = q.Question.difficulty
            questions['category'] = q.Question.category
            ques_dic['current_category'] = q.Category.type
            ques_dic['questions'].append(questions.copy())
        ques_dic['total_questions'] = data_ques.count()
        for cat in Category.query.all():
            data_cat[cat.id] = cat.type
        return jsonify({'sucess': True, 'current_category': ques_dic['current_category'], 'questions': ques_dic['questions'], 'categories': data_cat, 'total_questions': ques_dic['total_questions']})

  # ***DONE***TEST: At this point, when you start the application
  # you should see questions and categories generated,
  # ten questions per page and pagination at the bottom of the screen for three pages.
  # Clicking on the page numbers should update the questions.

  # ***DONE***@TODO:
  # Create an endpoint to DELETE question using a question ID.

    @ app.route('/questions/<int:q_id>', methods=['DELETE'])
    def delete_question(q_id):
        # page = request.args.get('page', 1, type=int)
        try:
            ques_to_delete = Question.query.filter(
                Question.id == q_id).one_or_none()
            if ques_to_delete is None:
                abort(422)
            ques_to_delete.delete()
            return jsonify({'sucess': True})
        except:
            abort(422)
  # ***DONE***TEST: When you click the trash icon next to a question, the question will be removed.
  # This removal will persist in the database and when you refresh the page.

  # ***DONE***@TODO:
  # Create an endpoint to POST a new question,
  # which will require the question and answer text,
  # category, and difficulty score.
    @ app.route('/add', methods=['POST'])
    def submitQuestion():
        question = request.get_json()['question']
        answer = request.get_json()['answer']
        category = request.get_json()['category']
        difficulty = request.get_json()['difficulty']
        try:
            new_ques = Question(question=question, answer=answer,
                                category=category, difficulty=difficulty)
            new_ques.insert()
            return jsonify({'success': True})
        except:
            abort(422)
  # ***DONE***TEST: When you submit a question on the "Add" tab,
  # the form will clear and the question will appear at the end of the last page
  # of the questions list in the "List" tab.

  # ***DONE***@TODO:
  # Create a POST endpoint to get questions based on a search term.
  # It should return any questions for whom the search term
  # is a substring of the question.

    @ app.route('/search-questions', methods=['POST'])
    def submitSearch():
        ques_srch_dic = {}
        quesSrch = {}
        ques_srch_dic['questions'] = []
        searchTerm = request.get_json()['searchTerm']
        searchTerm = '%'+searchTerm+'%'
        search_ques = Question.query.filter(
            Question.question.ilike(searchTerm))
        ques_srch_dic['total_questions'] = search_ques.count()
        for ques_res in search_ques:
            quesSrch['id'] = ques_res.id
            quesSrch['question'] = ques_res.question
            quesSrch['answer'] = ques_res.answer
            quesSrch['difficulty'] = ques_res.difficulty
            quesSrch['category'] = ques_res.category
            ques_srch_dic['current_category'] = ques_res.category
            ques_srch_dic['questions'].append(quesSrch.copy())
        return jsonify({'sucess': True, 'questions': ques_srch_dic['questions'], 'total_questions': ques_srch_dic['total_questions'], 'current_category': ques_srch_dic['current_category']})

  # ***DONE***TEST: Search by any phrase. The questions list will update to include
  # only question that include that string within their question.
  # Try using the word "title" to start.

  # ***DONE***@TODO:
  # Create a GET endpoint to get questions based on category.

    @ app.route('/categories/<int:cat_id>/questions', methods=['GET'])
    def getByCategory(cat_id):
        ques_by_cat_dic = {}
        quesByCat = {}
        ques_by_cat_dic['questions'] = []
        ques_by_cat = Question.query.filter(
            Question.category == cat_id)
        for ques_cat_res in ques_by_cat:
            quesByCat['id'] = ques_cat_res.id
            quesByCat['question'] = ques_cat_res.question
            quesByCat['answer'] = ques_cat_res.answer
            quesByCat['difficulty'] = ques_cat_res.difficulty
            quesByCat['category'] = ques_cat_res.category
            ques_by_cat_dic['questions'].append(quesByCat.copy())
        ques_by_cat_dic['total_questions'] = ques_by_cat.count()
        return jsonify({'sucess': True, 'questions': ques_by_cat_dic['questions'], 'total_questions': ques_by_cat_dic['total_questions'], 'current_category': cat_id})

  # ***DONE***TEST: In the "List" tab / main screen, clicking on one of the
  # categories in the left column will cause only questions of that
  # category to be shown.

  # ***DONE***@TODO:
  # Create a POST endpoint to get questions to play the quiz.
  # This endpoint should take category and previous question parameters
  # and return a random questions within the given category,
  # if provided, and that is not one of the previous questions.

    @ app.route('/play', methods=['POST'])
    def getNextQuestion():
        ques_quiz_dic = {}
        prev_ques_list = []
        quiz_cat_dic = request.get_json()['quiz_category']
        quiz_cat_id = quiz_cat_dic['id']
        print("json", request.get_json())
        print("quiz_cat_id", quiz_cat_id)
        print("prev ques", request.get_json()['previous_questions'])

        if(request.get_json()['previous_questions'] is not None):
            prev_ques_list = request.get_json()['previous_questions']
            quiz_res = Question.query.filter(Question.category == quiz_cat_id, Question.id.notin_(
                prev_ques_list)).order_by(func.random()).limit(1)
        if(quiz_cat_id == 0):
            quiz_res = Question.query.order_by(func.random()).limit(1)

        for ques_res_obj in quiz_res:
            ques_quiz_dic = {'id': ques_res_obj.id, 'question': ques_res_obj.question,
                             'answer': ques_res_obj.answer, 'difficulty': ques_res_obj.difficulty, 'category': ques_res_obj.category}
        print("total", quiz_res.count())
        return jsonify({'success': True, 'question': ques_quiz_dic, 'total_questions': quiz_res.count()})

  # ***DONE*** TEST: In the "Play" tab, after a user selects "All" or a category,
  # one question at a time is displayed, the user is allowed to answer
  # and shown whether they were correct or not.

  # ***DONE***@TODO:
  # Create error handlers for all expected errors
  # including 400, 404, 422 and 500..
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422
    return app

    @app.errorhandler(400)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400
    return app

    @app.errorhandler(500)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500
    return app
