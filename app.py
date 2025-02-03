from fastapi import FastAPI, Query, HTTPException
import requests
from pydantic import BaseModel, validator
from typing import List

app = FastAPI()

# Define response models
class NumberResponse(BaseModel):
    number: int
    is_prime: bool
    is_perfect: bool
    properties: List[str]
    digit_sum: int
    fun_fact: str

    @validator("properties")  # Ensure consistent order
    def validate_properties(cls, properties):
        if "armstrong" in properties:
            return ["armstrong"] + [p for p in properties if p != "armstrong"]  # armstrong first
        return properties

class ErrorResponse(BaseModel):
    number: str
    error: bool = True

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_armstrong(n: int) -> bool:
    digits = [int(d) for d in str(n)]
    power = len(digits)
    return sum(d**power for d in digits) == n

def is_perfect(n: int) -> bool:
    if n <= 0:
        return False
    return sum(i for i in range(1, n) if n % i == 0) == n

def get_fun_fact(n: int) -> str:  # No longer needs is_armstrong_num
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math?json", timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get("text", "No fun fact available.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching fun fact: {e}")
        return "No fun fact available."

@app.get("/api/classify-number", response_model=NumberResponse, responses={400: {"model": ErrorResponse}})
async def classify_number(number: str = Query(...)):
    try:
        num = int(number) # Directly convert to int, handle ValueError if not an int
    except ValueError:
        return ErrorResponse(number=number)

    properties = []
    if is_armstrong(num):
        properties.append("armstrong")
    if num % 2 != 0:
        properties.append("odd")
    else:
        properties.append("even")

    response_data = {
        "number": num,
        "is_prime": is_prime(num),
        "is_perfect": is_perfect(num),
        "properties": properties,
        "digit_sum": sum(int(d) for d in str(abs(num))),
        "fun_fact": get_fun_fact(num)
    }

    return response_data