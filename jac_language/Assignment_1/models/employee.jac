"""
Employee Interface Definition
Defines the contract for employee-related functionality
"""

# Abstract Employee Interface
 obj Employee {
    has id: str;
    has name: str;
    has department: str;
    has salary: float;
    has years_of_service: int;

    # Core methods that implementations must provide
     def display_info();
    def calculate_annual_compensation()  -> float;
    def is_eligible_for_promotion()  -> bool;
}


# Extended interface for crew members with additional space-specific features
 obj CrewMember(Employee) {
    has rank: str;
    has missions_completed: int = 0;
    has clearance_level: str = "Standard";

    # Additional crew-specific methods
     def promote(new_rank: str, salary_increase: float);
    def grant_bonus(amount: float);
    def is_senior_crew()  -> bool;
    def complete_mission();
}
