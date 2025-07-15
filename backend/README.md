# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## API Endpoints Documentation

### `GET '/categories'`

- **Description**: Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- **Request Arguments**: None
- **Returns**: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

**Response Example:**
```json
{
  "success": true,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

**Error Response:**
- `500` - Internal server error

---

### `GET '/questions'`

- **Description**: Fetches a paginated list of questions with optional pagination parameters
- **Request Arguments**: 
  - `page` (optional): Page number (default: 1)
  - `per_page` (optional): Number of questions per page (default: 10)
- **Returns**: An object containing questions, total count, categories

**Request Example:**
```
GET /questions?page=1&per_page=10
```

**Response Example:**
```json
{
  "success": true,
  "questions": [
    {
      "id": 1,
      "question": "What is the capital of France?",
      "answer": "Paris",
      "category": 3,
      "difficulty": 1
    }
  ],
  "total_questions": 50,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment", 
    "6": "Sports"
  },
}
```

**Error Response:**
- `500` - Internal server error

---

### `DELETE '/questions/<int:question_id>'`

- **Description**: Deletes a specific question by its ID
- **Request Arguments**: 
  - `question_id` (path parameter): The ID of the question to delete
- **Returns**: An object confirming the deletion

**Request Example:**
```
DELETE /questions/1
```

**Response Example:**
```json
{
  "success": true,
  "deleted": 1
}
```

**Error Response:**
- `404` - Question not found
- `500` - Internal server error

---

### `POST '/questions'`

- **Description**: Creates a new question with the provided data
- **Request Body**: JSON object containing question, answer, category, and difficulty
- **Returns**: An object confirming the creation with the new question ID

**Request Body:**
```json
{
  "question": "What is the largest planet in our solar system?",
  "answer": "Jupiter",
  "category": 1,
  "difficulty": 2
}
```

**Response Example:**
```json
{
  "success": true,
  "created": 25
}
```

**Error Response:**
- `400` - Bad request (missing required fields)
- `500` - Internal server error

---

### `POST '/questions/search'`

- **Description**: Searches for questions containing the specified search term
- **Request Body**: JSON object containing the search term
- **Returns**: An object containing matching questions and total count

**Request Body:**
```json
{
  "searchTerm": "capital"
}
```

**Response Example:**
```json
{
  "success": true,
  "questions": [
    {
      "id": 1,
      "question": "What is the capital of France?",
      "answer": "Paris",
      "category": 3,
      "difficulty": 1
    },
    {
      "id": 15,
      "question": "What is the capital of Japan?",
      "answer": "Tokyo",
      "category": 3,
      "difficulty": 2
    }
  ],
  "total_questions": 2
}
```

**Error Response:**
- `400` - Bad request (missing search term)
- `500` - Internal server error

---

### `GET '/categories/<string:category_id>/questions'`

- **Description**: Fetches all questions for a specific category
- **Request Arguments**: 
  - `category_id` (path parameter): The ID of the category
- **Returns**: An object containing questions for the specified category

**Request Example:**
```
GET /categories/1/questions
```

**Response Example:**
```json
{
  "success": true,
  "questions": [
    {
      "id": 1,
      "question": "What is the largest planet in our solar system?",
      "answer": "Jupiter",
      "category": 1,
      "difficulty": 2
    },
    {
      "id": 2,
      "question": "What is the chemical symbol for gold?",
      "answer": "Au",
      "category": 1,
      "difficulty": 1
    }
  ]
}
```

**Error Response:**
- `500` - Internal server error

---

### `POST '/quizzes'`

- **Description**: Gets a random question for the quiz, excluding previously asked questions
- **Request Body**: JSON object containing quiz category and previous questions
- **Returns**: An object containing a random question

**Request Body:**
```json
{
  "quiz_category": {
    "id": 1,
    "type": "Science"
  },
  "previous_questions": [1, 4, 20]
}
```

**Response Example:**
```json
{
  "success": true,
  "question": {
    "id": 15,
    "question": "What is the chemical symbol for oxygen?",
    "answer": "O",
    "category": 1,
    "difficulty": 1
  }
}
```

**Error Response:**
- `400` - Bad request (missing category information)
- `500` - Internal server error

## Error Handling

The API includes comprehensive error handling for the following scenarios:

- **400 Bad Request**: Invalid request data or missing required fields
- **404 Not Found**: Requested resource not found
- **422 Unprocessable Entity**: Request cannot be processed
- **500 Internal Server Error**: Server-side error

All error responses follow this format:
```json
{
  "success": false,
  "error": 400,
  "message": "Bad request"
}
```

## Testing
To run the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
