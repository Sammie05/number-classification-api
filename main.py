import math
import requests
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Union

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    sqrt_n = math.isqrt(n)
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    if n <= 1:
        return False
    total = 1
    sqrt_n = math.isqrt(n)
    for i in range(2, sqrt_n + 1):
        if n % i == 0:
            total += i
            if i != n // i:
                total += n // i
    return total == n

def is_armstrong(n: int) -> bool:
    digits = str(abs(n))
    length = len(digits)
    return n == sum(int(d)**length for d in digits)

def get_digit_sum(n: int) -> int:
    return sum(int(d) for d in str(n) if d.isdigit())

def get_parity(n: int) -> str:
    return "even" if n % 2 == 0 else "odd"

@app.get("/api/classify-number", response_model=dict)
async def classify_number(
    number: Union[str, None] = Query(default=None, title="Number to classify")
):
    # Validate input
    if not number:
        raise HTTPException(status_code=400, detail={"number": None, "error": True})
    
    try:
        num = int(number)
    except ValueError:
        return {
            "number": number,
            "error": True
        }

    # Calculate properties
    properties = []
    
    if is_armstrong(num):
        properties.append("armstrong")
    
    properties.append(get_parity(num))
    
    # Get fun fact
    try:
        response = requests.get(f"http://numbersapi.com/{num}/math".format(number=num), timeout=2)
        fun_fact = response.text if response.status_code == 200 else f"{num} is a number."
    except requests.exceptions.RequestException:
        fun_fact = f"{num} is a number."

    return {
        "number": num,
        "is_prime": is_prime(num),
        "is_perfect": is_perfect(num),
        "properties": properties,
        "digit_sum": get_digit_sum(num),
        "fun_fact": fun_fact
    }

@app.get("/")
async def root():
    return {"message": "Welcome to the Number Classification API! Use /api/classify-number?number=123 to classify a number."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
