# calculator practice with object oriented programming in jac

obj Calculator {
  has history: list[str] = [];

  def add(a: float, b: float) -> float {
    result: float = a + b;
    self.history.append(result);
    return result;
  }

  def subtract(a: float, b: float) -> float {
    result: float = a - b;
    self.history.append(result);
    return result;
  }

  def product(a: float, b: float) -> float {
    result: float = a * b;
    self.history.append(result);
    return result;
  }

  def division(a: float, b: float) -> float {
    result: float = a / b;
    self.history.append(result);
  }

  def get_history() -> list[str] {
    return self.history;
  }

  def clear_hitory() {
    self.history = [];
  }
}

with entry {
    print("-----Your basic calculator----");

    #instatiate the class
    calc = Calculator();
    
    num1: float = 32.0;
    num2: float = 8.0;

    #perform calculations
    result1: float = calc.add(num1, num2);
    result2: float = calc.subtract(num1, num2);
    result3: float = calc.product(num1, num2);
    result4: float = calc.division(num1, num2);

    print(f"{result1}, {result2}, {result3}, {result4}");

    #get history
    print("\nCalculation history");
    for result in calc.get_history() {
      print(f"{result}");
    }
  }