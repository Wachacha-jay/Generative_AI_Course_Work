def add(a: float, b:float) -> float {
  return a + b;
}

def subtraction(a: float, b:float) -> float {
  return a - b;
}

def product(a: float, b:float) -> float {
  return a * b;
}

def division(a: float, b:float) -> float {
  
  return a / b;
}

with entry {
    print("=== Simple Calculator ===");

    # Test calculations
    num1: float = 10.0;
    num2: float = 0.0;

    print(f"{num1} + {num2} = {add(num1, num2)}");
    print(f"{num1} - {num2} = {subtraction(num1, num2)}");
    print(f"{num1} * {num2} = {product(num1, num2)}");
    try {
      result: float = division(num1, num2);
      print(f"{num1} / {num2} = {result}");
    } except ZeroDivisionError {
      print("Number cannot be divided by 0");
    }      
}