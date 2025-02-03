from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Functions
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    if n < 2:
        return False
    divisors = [i for i in range(1, n) if n % i == 0]
    return sum(divisors) == n

def is_armstrong(n):
    digits = [int(d) for d in str(n)]
    length = len(digits)
    return sum(d**length for d in digits) == n

def digit_sum(n):
    return sum(int(d) for d in str(n))

def get_fun_fact(n):
    url = f"http://numbersapi.com/{n}/math"
    response = requests.get(url)
    return response.text  # Directly return the API response text

# Main endpoint
@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    print("API called")
    number = request.args.get('number')

    # Input validation
    if not number:
        return jsonify({"number": "null", "error": True}), 400
    
    if number.isdigit() or (number.startswith('-') and number[1:].isdigit()):
        number = int(number)
    elif number.isalpha():
        return jsonify({"number": "alphabet", "error": True}), 400
    else:
        return jsonify({"number": "number and alphabet", "error": True}), 400
    
    # Determine properties
    properties = []
    if is_armstrong(number):
        properties.append("armstrong")
    if number % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")
   
    response = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": digit_sum(number),
        "fun_fact": get_fun_fact(number)  
    }
    
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)