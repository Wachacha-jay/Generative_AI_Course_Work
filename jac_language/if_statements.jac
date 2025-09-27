def employee_salary(designation: str) -> float{
  if designation == "manager" {
    return 100000.00;
  } elif designation == "supervisor" {
    return 80000.00;
  } elif designation == "accountant" {
    return 75000.00;
  } else {
    return 50000.00;
  }
}
with entry {
  #employee list
  employees: dict[str, str] = {"Michael": "manager",
  "Dwight": "supervisor",
  "Angela": "accountant",
  "pam": "supervisor"};

  #payrol generation
  payrol: dict[str, float] = {employee: employee_salary(title) for employee, title in employees.items()};
  
  print(f"This is january's payrol: {payrol}");

}