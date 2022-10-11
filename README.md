# Trivia App

Trivia is a web application designed to host trivia games. Trivia was built to breach the gap between employees and students, by allowing them engage in trivia activities, Thereby promoting good relationship between stakeholders at Udacity. Trivia is intigrated with an API built that provide resources needed to power the web application.


## Getting Started
The instruction below may be followed to setup the project on your local machine.

### Prerequisites

Backend
1. Python 3.8
2. Virtual Environment
3. Postgresql

Frontend
1. NodeJS

### Installations

- Step 1: Install prerequisites software

- Step 2: Install frontend dependencies
After the repository zip file has been extracted, Open Terminal (or command line on windows) and navigate to the project directory. Further navigate to the frontend directory and install frontend dependencies with the command below:

npm install

- Step 3: Create virtual environment
Create a virtual environment for backend dependencies. navigate to the backend directory and use the command below to create a virtual environment and activate the source:

python3 -m venv projectenv
source projectenv\bin\activate

- Step 4: Install backend dependencies
Install backend dependencies by running the command below in the `backend` directory:

pip install -r requirements.txt

- Step 5: configure database
Start Postgresql DBMS on terminal with the command below:

sudo systemctl start postgresql.service

Create production and test database:

createdb trivia
createdb trivia_test

Populate both production/development and test database with  database dumps files.

psql trivia < trivia.psql
psql trivia_test < trivia.psql

### Starting up the Server
Make sure the virtual environment is activated. Navigate to the backend directory and run the following command to start the backend server.

export FLASK_APP=flaskr
export FLASK_ENV=development
flask run

Similarly, navigate to the frontend directory and run the following command to start the frontend server.

npm start

### Running API test
Test API by Executing the test_flaskr.py python file in the backend directory.

python3 test_flaskr.py

## API Reference
Trivia can be accessed with a web browser via the base URL below.
Trivia base URL: localhost:5000

### Error status codes and message
400 - Invalid request
422 - Sorry, could not process your request
404 - Requested resource not found
500 - Server error

- Error response example
{
    'success': False,
    'error': 404,
    'message': 'Requested resource not found'
}

### API Endpoints

#### GET '/categories'

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs.
{
    'success': True,
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" }
}
#### GET '/questions?page=${integer}'

- Fetches a paginated set of questions, a total number of questions, all categories and current category string.
- Request Arguments: page - integer
- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string

{
    'success': True,
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 2
        },
    ],
    'totalQuestions': 100,
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" },
    'currentCategory': 'History'
}


#### GET '/categories/${id}/questions'

- Fetches questions for a cateogry specified by id request argument
- Request Arguments: id - integer
- Returns: An object with questions for the specified category, total questions, and current category string

{
    'success': True,
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 4
        },
    ],
    'totalQuestions': 100,
    'currentCategory': 'History'
}


#### DELETE '/questions/${id}'

- Deletes a specified question using the id of the question
- Request Arguments: id - integer
- Returns: Does not need to return anything besides the appropriate HTTP status code. Optionally can return the id of the question. If you are able to modify the frontend, you can have it remove the question using the id instead of refetching the questions.


#### POST '/quizzes'

- Sends a post request in order to get the next question
- Request Body:

{
    'previous_questions': [1, 4, 20, 15]
    quiz_category': 'current category'
 }

- Returns: a single new question object

{
    'success': True,
    'question': {
        'id': 1,
        'question': 'This is a question',
        'answer': 'This is an answer',
        'difficulty': 5,
        'category': 4
    }
}


#### POST '/questions'

- Sends a post request in order to add a new question
- Request Body:

{
    'question':  'Heres a new question string',
    'answer':  'Heres a new answer string',
    'difficulty': 1,
    'category': 3,
}

- Returns: 
{
    'success': True
}


#### POST '/search'

- Sends a post request in order to search for a specific question by search term
- Request Body:

{
    'searchTerm': 'this is the term the user is looking for'
}

- Returns: any array of questions, a number of totalQuestions that met the search term and the current category string

{
    'success': True,
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 5
        },
    ],
    'totalQuestions': 100,
    'currentCategory': 'Entertainment'
}

## Authors
- Nazif Abdulkadir
- Sarah Maris
- Sudhanshu Kulshrestha
- UAnjali

## Acknowledgements
I will like to thank Udacity and ALX for giving me the opportunity to be a part of this program and also special thank to the course instructor, Caryn McCarthy for her efforts in making it easy to gasp the concepts in the course.
