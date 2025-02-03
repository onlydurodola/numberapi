from flask import Flask, request, jsonify
import requests

app = Flask(_name_)

# Prime check (unchanged)
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# Armstrong check (unchanged)
def is_armstrong(n):
    digits = [int(d) for d in str(n)]
    power = len(digits)
    return sum(d ** power for d in digits) == n

# Perfect number check (unchanged)
def is_perfect(n):
    if n <= 0:  
        return False
    return sum(i for i in range(1, n) if n % i == 0) == n

# Fun fact (unchanged)
def get_fun_fact(n):
    response = requests.get(f"http://numbersapi.com/{n}/math?json")
    if response.status_code == 200:
        return response.json().get("text", "No fun fact available.")
    return "No fun fact available."

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number_str = request.args.get('number')
    
    # Validate input as numeric
    try:
        num_float = float(number_str)
    except (ValueError, TypeError):
        return jsonify({
            "number": number_str,
            "error": "Invalid input: not a number"
        }), 400

    # Ensure it's an integer (whole number)
    if not num_float.is_integer():
        return jsonify({
            "number": num_float,
            "error": "Number must be an integer (no decimal)"
        }), 400

    num = int(num_float)  # Convert to integer for processing

    # Rest of the logic remains the same
    properties = []
    if is_armstrong(num):
        properties.append("armstrong")
    properties.append("odd" if num % 2 != 0 else "even")

    response_data = {
        "number": num,
        "is_prime": is_prime(num),
        "is_perfect": is_perfect(num),
        "properties": properties,
        "digit_sum": sum(int(d) for d in str(abs(num))),  # Fix: Use abs()
        "fun_fact": get_fun_fact(num)
    }

    return jsonify(response_data)

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=5000, debug=True)