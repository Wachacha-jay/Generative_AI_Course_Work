import datetime from {datetime};

glob employee_name: str = "michael scott";
glob employee_code: int = 108;
glob designation: str = "manager";

def years_worked() -> int {
  employee_start_date: int = 1987;
  current_time: int = datetime.now();
  return current_time - employee_start_date;

}

def get_salary(designation: str) -> float {
  if designation == "manager" {
    return 100000.00;
  }
}

with entry {
    print("employee_name");
    print(years_worked());
    print(f"My salary is kes{get_salary()}");
}