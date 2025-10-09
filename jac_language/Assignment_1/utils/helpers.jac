"""
Helper Functions
Utility functions for the crew management system
"""

import from utils.constants { BONUS_BASE_RATE, SENIOR_BONUS_MULTIPLIER, SENIOR_CREW_THRESHOLD }


#* Format currency values for display
 def format_currency(amount: float) -> str {
    return "$" + amount;
}*#
 # Print a formatted header
 def print_header(title: str) {
    let width = len(title) + 4;
    let border = "=" * width;
    print(f"\n{border}");
    print(f"  {title}");
    print(f"{border}\n");
}


# Calculate performance bonus based on salary and service
 def calculate_bonus(
    salary: float,
    years_of_service: int
) -> float {
    let base_bonus = salary * BONUS_BASE_RATE;
    # Senior crew members get enhanced bonuses
     if years_of_service >= SENIOR_CREW_THRESHOLD {
        return base_bonus * SENIOR_BONUS_MULTIPLIER;
    }
    return base_bonus;
}


# Validate employee ID format (EMP + 3 digits)
 def validate_employee_id(id: str) -> bool {
    if len(id) != 6 {
        return false;
    }
    if not id[ : 3 ] == "EMP" {
        return false;
    }
    # Check if last 3 characters are digits
    let num_part =
        id[ 3 : ];
    return num_part.isdigit();
}


# Calculate years until retirement (assuming retirement at 30 years)
 def years_to_retirement(
    years_of_service: int
) -> int {
    let retirement_years = 30;
    let remaining = retirement_years - years_of_service;
    return remaining if remaining > 0 else 0;
}


# Generate a crew report summary
 def generate_crew_summary(crew_list: list) -> dict {
    let total_salary = 0;
    let total_years = 0;
    let departments = {};
    for member in crew_list {
        total_salary += member.salary;
        total_years += member.years_of_service;
        # Count by department
         if member.department in departments {
            departments[member.department] += 1;
        } else {
            departments[member.department] = 1;
        }
    }
    return
    {"total_crew" : len(crew_list) , "total_payroll" : total_salary , "average_years" : total_years / len(crew_list) if len(crew_list) > 0 else 0 , "departments" : departments };
}


# Rank crew members by experience
 def rank_by_experience(crew_list: list) -> list {
    # Simple bubble sort by years of service
    let sorted_crew =
        crew_list[ : ];
    # Copy the list
    let n =
        len(sorted_crew);
    for i in range(n) {
        for j in range(0, n - i - 1) {
            if sorted_crew[j].years_of_service < sorted_crew[j + 1].years_of_service {
                # Swap
                let temp =
                    sorted_crew[j];
                sorted_crew[j] = sorted_crew[j + 1];
                sorted_crew[j + 1] = temp;
            }
        }
    }
    return sorted_crew;
}


# Calculate department budget allocation
 def calculate_department_budget(
    crew_list: list,
    department: str
) -> float {
    let dept_budget = 0;
    for member in crew_list {
        if member.department == department {
            dept_budget += member.salary;
        }
    }
    return dept_budget;
}


# Format service years into a readable string
 def format_service_time(years: int) -> str {
    if years == 0 {
        return "New recruit";
    } elif years == 1 {
        return "1 year";
    } elif years < 5 {
        return f"{years} years (Junior)";
    } elif years < 10 {
        return f"{years} years (Experienced)";
    } else {
        return f"{years} years (Veteran)";
    }
}
