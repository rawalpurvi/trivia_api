The Trivia of Udacity

The API is to play the Trivia game. User can play a game upto 5 questions. They can play the Trivia game for any specific category or all categories and at the end they will get a score. There are 6 predifined categoies like Science, Art, Geography, History, Entertainment, Sports. User can add questions. They can add question along with answer, difficulty, rating and category. To play the Trivia game user needs atleast 6 questions per category.  


Getting Started

    ## Pre-requisites and Local Development

    Run this project one should have Python3, pip and node installed on their local machines.

    ## Back end     

    From the backend folder run pip install requirements.txt . All required packages are included in the requirenments file. 

    To run the application run the following commands:

    export FLASK_APP=flaskr
    export FLASK_ENV=development
    flask run

    The application is run on http://127.0.0.1:5000/ by default and a proxy in the frontend configuration.

    ## Front end

    From the frontend folder, run the following commands to start the client:

    npm install //only once to install dependencies 
    npm start

    By default, the front end will run on localhost:3000.

    ## Tests

    In order to run tests nevigate to the backend folder and the following commands:

    dropdb trivia_test
    createdb trivia_test
    psql trivia_test < trivia.psql
    python test_flaskr.py 

    The first time run the tests, omit the dropdb command.

    All tests are kept in the file and should be maintained as updates are made to app functionality.

API Preference

    ## Getting Started

    Base Url: At present this app can only be run locally and is not hosted as a base url. The backend app is hosted at the default, http://127.0.0.1:5000/ , which is set as a proxy in the frontend configurations.

    Authentication: This version of the application does not require authentication or API keys.

    ## Error Handling

    Errors are returned as JSON objects in the following format:
    {
        "error": 404, 
        "message": "resource not found", 
        "success": false
    }

    The API will return five types of error when requests fail:

    1. 400: Bad Request
    2. 404: Resource Not Found
    3. 405: Method Not Allowed
    4. 422: Unprocessable
    5. 500: Internal Server Error     

    ## Endpoints

    1. Get categories

    GET '/categories'
    - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
    - Request Arguments: None
    - Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
    - curl http://127.0.0.1:5000/categories
    {
        "categories": {
            "1": "Science", 
            "2": "Art", 
            "3": "Geography", 
            "4": "History", 
            "5": "Entertainment", 
            "6": "Sports"
        }, 
        "success": true
    } 

    2. Get questions

    GET '/questions'
    - Fetched all the questions with answer, difficulty and category
    - Request Arguments: None
    - This request also works pagination to show questions like '/questons?page=1'
    - Pagination show 10 quetions per Page
    - Returns: object questoins, total question, current_category, categories
    - curl http://127.0.0.1:5000/questions OR curl http://127.0.0.1:5000/questions?page=2
    {
        "categories": {
            "1": "Science", 
            "2": "Art", 
            "3": "Geography", 
            "4": "History", 
            "5": "Entertainment", 
            "6": "Sports"
        }, 
        "current_category": "Science", 
        "questions": [
          {
            "id": 1, 
            "question": "What is reaponsible for the moon-s phases?",
            "answer": "The Earth-Sun-Moon system", 
            "category": "1", 
            "difficulty": 4, 
            "rating": 2
          }, 
          :
          :
          :
          {
            "id": 10, 
            "question": "WHAT WOULD LIFE BE WITHOUT ART?",  
            "answer": "Whatever is difficult to find in life is possible in the arts", 
            "category": "2", 
            "difficulty": 1, 
            "rating": 3 
          }
        ], 
        "success": true, 
        "total_questions": 37
    }

    3. Delete Question

    DELETE '/questions/<int:question_id>'
    - Delete question form database using question id
    - Request Argument: question_id
    - Return deleted question.id, current_questions, total question
    - Pagination show 10 quetions per Page
    - curl -X DELETE http://127.0.0.1:5000/questions/6 
    {
        "deleted": 6, 
        "questions": [
           {
            "id": 1, 
            "question": "What is reaponsible for the moon-s phases?",
            "answer": "The Earth-Sun-Moon system", 
            "category": "1", 
            "difficulty": 4,
            "rating": 2
          },
          :
          :
          :
          {
            "id": 11, 
            "question": "WHAT WOULD LIFE BE WITHOUT ART?", 
            "answer": "Whatever is difficult to find in life is possible in the arts", 
            "category": "2", 
            "difficulty": 1,
            "rating": 3 
          }
        ], 
        "success": true, 
        "total_questions": 37
    }

    4. Add Question

    POST '/questions'
    - Request Data: question, answer, category, difficulty
    - Add new question into database
    - The added question can be shown at the end of the list
    - Return id of created question, questions, total questions
    - Pagination show 10 quetions per Page
    - curl -X POST -H "Content-Type:application/json" -d '{"question":"What is the most used color in Art?", "answer":"Black", "category":2, "difficulty":1, "rating": 4}' http://127.0.0.1:5000/questions
    {
        "created": 47, 
        "questions": [
          {
            "id": 1, 
            "question": "What is reaponsible for the moon-s phases?",  
            "answer": "The Earth-Sun-Moon system", 
            "category": "1", 
            "difficulty": 4,
            "rating": 2
          }, 
          :
          :
          :
          {
            "id": 10, 
            "question": "WHAT WOULD LIFE BE WITHOUT ART?",  
            "answer": "Whatever is difficult to find in life is possible in the arts", 
            "category": "2", 
            "difficulty": 1,
            "rating": 3 
         }
      ], 
      "success": true, 
      "total_questions": 38
    }

    5. Search 

    POST '/search'
    - Search endpoint will search from the question
    - Request Argument: searchTerm
    - Return questions object with searchTerm and total_questoins
    - curl -X POST -H "Content-Type:application/json" -d '{"searchTerm":"can"}' http://127.0.0.1:5000/search
    {
    "questions": [
        {
            "id": 4, 
            "question": "Can you see a New Moon?",  
            "answer": "No", 
            "category": "1", 
            "difficulty": 1,
            "rating": 3
        }, 
        {
            "id": 15, 
            "question": "CAN ANYBODY BE AN ARTIST?",  
            "answer": "Yes", 
            "category": "2", 
            "difficulty": 1,
            "rating": 1
        }, 
        {
            "id": 27, 
            "question": "How many stars does the American Flag have?",  
            "answer": "50", 
            "category": "4", 
            "difficulty": 1,
            "rating": 4 
        }
      ], 
      "success": true, 
      "total_questions": 3
    }

    6. Get questions for specific category

    GET '/categories/<int:category_id>/questions'
    - This endpoint gets all the questions for specific category
    - Request Argument: categry_id
    - Return questions object, total questions
    - curl http://127.0.0.1:5000/categories/3/questions
    {
      "questions": [
        {
            "id": 17, 
            "question": "What is Earth's largest continent?",  
            "answer": "Asia", 
            "category": "3", 
            "difficulty": 3,
            "rating": 2
        }, 
        {
            "id": 20, 
            "question": "What is the biggest state in the US?",  
            "answer": "Alaska", 
            "category": "3", 
            "difficulty": 2,
            "rating": 1 
        }, 
        {
            "id": 40, 
            "question": " What is the driest place on Earth?",   
            "answer": "McMurdo,Antactica", 
            "category": "3", 
            "difficulty": 4,
            "rating": 5
        }
      ], 
      "success": true, 
      "total_questions": 3
    }


    7. Get question for trivia quiz

    POST '/quizzes'
    - This endpoint gives randdom question to paly quiz
    - If user choose specific category question will come within the chosen category and it will be not from the previous questions
    - Return object question
    - curl -X POST -H "Content-Type:application/json" -d '{"previous_questions":"1", "quiz_category":{"id":3,"type":"Geography"}}' http://127.0.0.1:5000/quizzes
    {
        "question": {
            "id": 17, 
            "question": "What is Earth's largest continent?",
            "answer": "Asia", 
            "category": "3", 
            "difficulty": 3,
            "rating": 2
        }, 
        "success": true
    }

Deployment N/A

Author

Udacity Student, Purvi Rawal

Acknoledgemnts

Udacity team for making a greate project framework for Trivia API. 
