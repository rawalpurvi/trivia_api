import os
from flask import Flask, request, abort, jsonify, flash
from flask_sqlalchemy import SQLAlchemy #, or_, notin_
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# Define function to paginate questions
def paginate_question(request,selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={r"/api/*": {"origins": "*"}})
  
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods','GET,POST,PATCH,DELETE,OPTIONS')
    return response


  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories():
    categories = Category.query.order_by(Category.id).all()

    # if there is no category assign
    if len(categories) == 0:
      abort(404)

    # Make an array to generate category name and id string
    category_type = {}
    for category in categories:
      category_type[category.id]=category.type
    
    # retrun array of categories name and id
    return jsonify({
      'success': True,
      'categories': category_type
    })



  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions', methods=['GET'])
  def get_questions():
    questions = Question.query.order_by(Question.id).all()

    # if there is no question assign
    if len(questions) == 0:
      abort(404)

    selection = Question.query.order_by(Question.id).all()
    current_questions = paginate_question(request, selection)

    # if the request page number is not valid 
    if len(current_questions) == 0:
      abort(404)

    # Get all the categories
    categories = Category.query.order_by(Category.id).all()

    # if there is no category assign
    if len(categories) == 0:
      abort(404)

    # Make an array to generate category name and id string
    start = 0
    category_type = {}
    for category in categories:
      if (start == 0):
         current_category = category.type
      category_type[category.id]=category.type
      start = start + 1

    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions':len(Question.query.all()),
      'current_category': current_category,
      'categories': category_type
    })  

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):

    body = request.get_json()

    try:
      question = Question.query.filter(Question.id==question_id).one_or_none()
      if question is None:
        abort(404)

      question.delete()
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_question(request, selection)

      return jsonify({
        'success': True,
        'deleted': question.id,
        'questions': current_questions,
        'total_questions':len(Question.query.all())
      })

    except:
      abort(400)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  
  @app.route('/questions', methods=['POST'])
  def add_question():
    body = request.get_json()

    try:
      # Add new question
      new_question = body.get("question", None)
      new_answer = body.get("answer", None)
      new_category = body.get("category", None)
      new_difficulty = body.get("difficulty", None)
      new_rating = body.get("rating", None)

      question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty, rating=new_rating)
      question.insert()

      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_question(request, selection)

      return jsonify({
            'success': True,
            'created': question.id,
            'questions': current_questions,
            'total_questions':len(Question.query.all())
      })
      
    except:
      abort(422)   

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  @app.route('/search', methods=['POST'])
  def search_question():
    body = request.get_json()

    search = body.get("searchTerm", None)
    
    # Search question
    selection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search))).all()
    questions = [question.format() for question in selection]

    #current_questions = paginate_question(request, selection)
        
    return jsonify({
      'success': True,
      'questions': questions,
      'total_questions': len(selection)
    })
          
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_specific_questions(category_id):
    
    selection = Question.query.filter_by(category=category_id).all()

    # If there is no question assign
    if len(selection) == 0:
      abort(404)

    current_questions = paginate_question(request, selection)
    # If page number is not valid 
    if len(current_questions) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions':len(current_questions),
    })  


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  @app.route('/quizzes', methods=['POST'])
  def play_trivia_quiz():
    body = request.get_json()

    # Get Json value
    previous_questions = body.get("previous_questions", None)
    quiz_category = body.get("quiz_category", None)
    
    # Check if previous questions are avilable and category    
    if previous_questions == [] and (quiz_category['id'] == 0):
      question = Question.query.first()
    elif previous_questions and (quiz_category['id'] == 0):
      question = Question.query.filter(Question.id.notin_(previous_questions)).first()
    elif (previous_questions is None) and (quiz_category['id'] != 0):
      question = Question.query.filter_by(category=quiz_category['id']).first()
    else:  
      question = Question.query.filter(Question.id.notin_(previous_questions), Question.category == quiz_category['id']).first()

    if question is None:
        abort(404)
    
    return jsonify({
      'success': True,
      'question': question.format()
    })  


  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'resource not found'
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'unprocessable'
    }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': 'bad request'
    }), 400

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      'success': False,
      'error': 405,
      'message': 'method not allowed'
    }), 405        
  
  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
      'success': False,
      'error': 500,
      'message': 'internal server error'
    }), 500        

  return app

    