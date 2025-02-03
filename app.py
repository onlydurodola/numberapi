from flask import Flask, request, jsonify
import requests
import json
app = Flask(_name_)
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True
def is_armstrong(n):
    digits = [int(d) for d in str(n)]
    power = len(digits)
    return sum(d ** power for d in digits) == n
def is_perfect(n):
    if n <= 0:
        return False
    return sum(i for i in range(1, n) if n % i == 0) == n
def get_fun_fact(n):
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math?json")
        response.raise_for_status()  # Raises an error for HTTP errors (e.g., 404)
        return response.json().get("text", "No fun fact available.")
    except (requests.RequestException, json.JSONDecodeError):
        return "No fun fact available."
@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number_str = request.args.get('number')
    if not number_str.isdigit() and not (number_str.startswith("-") and number_str[1:].isdigit()):
        return jsonify({"number": number_str, "error": "Invalid input: not an integer"}), 400
    num = int(number_str)
    properties = ["odd" if num % 2 != 0 else "even"]
    if is_armstrong(num):
        properties.append("armstrong")
    response_data = {
        "number": num,
        "is_prime": is_prime(num),
        "is_perfect": is_perfect(num),
        "properties": properties,
        "digit_sum": sum(int(d) for d in str(abs(num))),
        "fun_fact": get_fun_fact(num)
    }
    response = jsonify(response_data)
    response.headers["Content-Type"] = "application/json"
    return response
if _name_ == '_main_':
    app.run(host='0.0.0.0', port=5000, debug=True)