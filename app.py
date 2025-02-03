from fastapi import FastAPI, Query, HTTPException
import requests
from pydantic import BaseModel
from typing import Dict, Any

app = FastAPI()

class NumberResponse(BaseModel):
    number: int
    is_prime: bool
    is_perfect: bool
    properties: list[str]
    digit_sum: int
    fun_fact: str

class ErrorResponse(BaseModel):
    number: str
    error: bool = True  # Default value for error

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_armstrong(n: int) -> bool:
    digits = [int(d) for d in str(n)]
    power = len(digits)
    return sum(d ** power for d in digits) == n

def is_perfect(n: int) -> bool:
    if n <= 0:
        return False
    return sum(i for i in range(1, n) if n % i == 0) == n

def get_fun_fact(n: int, is_armstrong_num: bool) -> str:
    if is_armstrong_num:
        digits = [int(d) for d in str(n)]
        power = len(digits)
        explanation = " + ".join([f"{d}^{power}" for d in digits])
        return f"{n} is an Armstrong number because {explanation} = {n}"
    response = requests.get(f"http://numbersapi.com/{n}/math?json")
    return response.json().get("text", "No fun fact available.") if response.ok else "No fun fact available."

@app.get("/api/classify-number", response_model=NumberResponse, responses={400: {"model": ErrorResponse}})
async def classify_number(number: str = Query(...)):
    try:
        num = float(number)
        if not num.is_integer():
            raise ValueError
        num = int(num)
    except ValueError:
        return ErrorResponse(number=number)

    armstrong = is_armstrong(num)
    properties = ["armstrong"] if armstrong else []
    properties.append("odd" if num % 2 else "even")

    response_data = {
        "number": num,
        "is_prime": is_prime(num),
        "is_perfect": is_perfect(num),
        "properties": properties,
        "digit_sum": sum(int(d) for d in str(abs(num))),
        "fun_fact": get_fun_fact(num, armstrong)
    }

    return response_data