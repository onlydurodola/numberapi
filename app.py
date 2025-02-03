from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Function to check if a number is prime
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# Function to check if a number is an Armstrong number
def is_armstrong(n):
    digits = [int(d) for d in str(n)]
    power = len(digits)
    return sum(d ** power for d in digits) == n

# Function to check if a number is perfect
def is_perfect(n):
    if n <= 0:  # Handle negative numbers and zero
        return False
    return sum(i for i in range(1, n) if n % i == 0) == n

# Function to get a fun fact about the number
def get_fun_fact(n):
    response = requests.get(f"http://numbersapi.com/{n}/math?json")
    if response.status_code == 200:
        return response.json().get("text", "No fun fact available.")
    return "No fun fact available."

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number = request.args.get('number')

    try:
        num = float(number) 
    except ValueError:
        return jsonify({"number": "alphabet", "error": True}), 400

    properties = []

    if is_armstrong(int(num)): 
        properties.append("armstrong")
    properties.append("odd" if int(num) % 2 != 0 else "even")

    response_data = {
        "number": num, # Return the original float number
        "is_prime": is_prime(int(num)) if num > 0 else False, 
        "is_perfect": is_perfect(int(num)), 
        "properties": properties,
        "digit_sum": sum(int(d) for d in str(int(num))) if num > 0 else 0, 
        "fun_fact": get_fun_fact(int(num)) 
    }

    return jsonify(response_data), 200 # Return 200 for all valid numbers

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)