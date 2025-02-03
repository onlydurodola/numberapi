from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
import requests
from typing import Union

app = FastAPI()

# Response models to enforce JSON structure and key order
class NumberResponse(BaseModel):
    number: int
    is_prime: bool
    is_perfect: bool
    properties: list[str]
    digit_sum: int
    fun_fact: str

class ErrorResponse(BaseModel):
    number: str
    error: bool = True

# Math validation functions
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
    return sum(d ** power for d in digits) == n

def is_perfect(n: int) -> bool:
    if n <= 0:
        return False
    return sum(i for i in range(1, n) if n % i == 0) == n

def generate_armstrong_fact(n: int) -> str:
    digits = [int(d) for d in str(n)]
    power = len(digits)
    terms = [f"{d}^{power}" for d in digits]
    return f"{n} is an Armstrong number because {' + '.join(terms)} = {n}"

# API endpoint
@app.get("/api/classify-number", 
         response_model=Union[NumberResponse, ErrorResponse],
         responses={400: {"model": ErrorResponse}})
async def classify_number(number: str = Query(...)):
    # Input validation
    try:
        num = float(number)
        if not num.is_integer():
            raise ValueError
        num = int(num)
    except ValueError:
        return ErrorResponse(number=number)
    
    # Calculate properties
    armstrong = is_armstrong(num)
    prime = is_prime(num)
    perfect = is_perfect(num)
    parity = "odd" if num % 2 else "even"
    
    # Build properties list
    properties = []
    if armstrong:
        properties.append("armstrong")
    properties.append(parity)
    
    # Generate fun fact
    fun_fact = generate_armstrong_fact(num) if armstrong else \
               requests.get(f"http://numbersapi.com/{num}/math").json().get("text", "No fun fact available")
    
    # Build response with ordered keys
    return {
        "number": num,
        "is_prime": prime,
        "is_perfect": perfect,
        "properties": properties,
        "digit_sum": sum(int(d) for d in str(abs(num))),
        "fun_fact": fun_fact
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0",  # Allow external access
        port=8000,        # Default FastAPI port
        log_level="debug" # Optional for troubleshooting
    )