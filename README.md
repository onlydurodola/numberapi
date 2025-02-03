Here’s a README.md tailored for your Number Classification API project:

# Number Classification API

A RESTful API that classifies a number and returns its mathematical properties (prime, perfect, Armstrong, odd/even) along with a fun fact sourced directly from the Numbers API(http://numbersapi.com/).

## Table of Contents
- [Features](#features)
- [API Endpoint](#api-endpoint)
- [Requirements](#requirements)
- [Installation](#installation)
- [Deployment](#deployment)
- [Testing](#testing)
- [Acknowledgments](#acknowledgments)

## Features
- **Mathematical Classification**:
  - Checks if a number is **prime**, **perfect**, or an **Armstrong number**.
  - Determines if the number is **odd** or **even**.
  - Calculates the **sum of its digits**.
- **Fun Fact Integration**: Directly fetches trivia from the [Numbers API](http://numbersapi.com/) without modification.
- **Error Handling**: Validates inputs and returns descriptive HTTP status codes.

## API Endpoint
### **GET** `/api/classify-number`
- **Query Parameter**: `number` (required).
- **Response Format**: JSON.

### Example Request
bash
GET /api/classify-number?number=371


### Example Success Response (200 OK)
json
{
    "number": 371,
    "is_prime": false,
    "is_perfect": false,
    "properties": ["armstrong", "odd"],
    "digit_sum": 11,
    "fun_fact": "371 is an Armstrong number because 3^3 + 7^3 + 1^3 = 371"
}


### Example Error Response (400 Bad Request)
json
{
    "number": "alphabet",
    "error": true
}


## Requirements
- Python 3.7+
- Flask
- Requests

## Installation
1. **Clone the Repository**:
   bash
   git clone https://github.com/onlydurodola/numberapi
   cd numberapi
   
2. **Install Dependencies**:
   bash
   pip install -r requirements.txt
   
3. **Run the API Locally**:
   bash
   python app.py
   
   The API will be accessible at `http://localhost:5000/api/classify-number?number=<number>`.

## Deployment
This API is deployed on [Render](https://render.com/). To deploy your own instance:
1. Create a `requirements.txt` file with:
   plaintext
   blinker==1.9.0
   certifi==2025.1.31
   charset-normalizer==3.4.1
   click==8.1.8
   Flask==3.1.0
   gunicorn==23.0.0
   idna==3.10
   itsdangerous==2.2.0
   Jinja2==3.1.5
   MarkupSafe==3.0.2
   packaging==24.2
   requests==2.32.3
   urllib3==2.3.0
   Werkzeug==3.1.3

OR

bash
  pip freeze > requirements.txt
   
   
2. Create a `Procfile` with:
   plaintext
   web: gunicorn -w 4 -b 0.0.0.0:$PORT app:app

   
3. Push your code to GitHub and deploy via Render.

**Public Endpoint**:  
`https://your-render-app-url.onrender.com/api/classify-number?number=<number>`

## Testing
### Using `curl`
bash
# Valid Request
curl "http://localhost:5000/api/classify-number?number=123"

# Invalid Request
curl "http://localhost:5000/api/classify-number?number=abc"

## Notes
- **Fun Fact Source**: The `fun_fact` field returns raw text from the [Numbers API](http://numbersapi.com/). No modifications are made.
- **Input Validation**: Only valid integers are processed. Non-integer inputs return a `400 Bad Request`.
- **Performance**: Response time is optimized to be under 500ms.

## Acknowledgments
- [Numbers API](http://numbersapi.com/) for providing fun math facts.
- Flask and Render for enabling easy deployment.


---

This README ensures clarity for users, testers, and collaborators. Let me know if you need adjustments! 🚀