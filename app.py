from flask import Flask, request, jsonify
import requests
from collections import OrderedDict

app = Flask(__name__)

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
    response = requests.get(f"http://numbersapi.com/{n}/math?json")
    if response.status_code == 200:
        return response.json().get("text", "No fun fact available.")
    return "No fun fact available."

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number_str = request.args.get('number')
    
    # Validate input as a number
    try:
        num_float = float(number_str)
    except (ValueError, TypeError):
        return jsonify(OrderedDict([
            ("number", number_str),
            ("error", True)
        ])), 400

    # Check if it's an integer
    if not num_float.is_integer():
        return jsonify(OrderedDict([
            ("number", num_float),
            ("error", True)
        ])), 400

    num = int(num_float)

    properties = []
    is_armstrong_num = is_armstrong(num)
    if is_armstrong_num:
        properties.append("armstrong")
    parity = "odd" if num % 2 != 0 else "even"
    properties.append(parity)

    # Generate fun fact for Armstrong numbers
    if is_armstrong_num:
        digits = [int(d) for d in str(num)]
        power = len(digits)
        sum_powers = sum(d ** power for d in digits)
        explanation = " + ".join([f"{d}^{power}" for d in digits]) + f" = {sum_powers}"
        fun_fact = f"{num} is an Armstrong number because {explanation}"
    else:
        fun_fact = get_fun_fact(num)

    response_data = OrderedDict([
        ("number", num),
        ("is_prime", is_prime(num)),
        ("is_perfect", is_perfect(num)),
        ("properties", properties),
        ("digit_sum", sum(int(d) for d in str(abs(num)))),
        ("fun_fact", fun_fact)
    ])

    return jsonify(response_data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)