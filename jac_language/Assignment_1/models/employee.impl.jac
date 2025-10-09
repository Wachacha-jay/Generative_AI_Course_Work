"""
Employee Implementation
Concrete implementation of the Employee and CrewMember interfaces
"""

import from utils.constants { SENIOR_CREW_THRESHOLD, PROMOTION_ELIGIBILITY_YEARS }


# Implement the Employee base functionality
 impl Employee.display_info{
    print(f"ID: {self.id}");
    print(f"Name: {self.name}");
    print(f"Department: {self.department}");
    print(f"Salary: {self.salary}");
    print(f"Years of Service: {self.years_of_service}");
}


impl Employee.calculate_annual_compensation -> float {
    # Base salary plus standard benefits (10% of salary)
     return self.salary * 1.10;
}


impl Employee.is_eligible_for_promotion -> bool {
    return self.years_of_service >= PROMOTION_ELIGIBILITY_YEARS;
}


# Implement CrewMember specific functionality
 impl CrewMember.display_info{
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
    print(f"👤 CREW MEMBER PROFILE");
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
    print(f"ID: {self.id}");
    print(f"Name: {self.name}");
    print(f"Rank: {self.rank}");
    print(f"Department: {self.department}");
    print(f"Clearance: {self.clearance_level}");
    print(f"Salary: {self.salary}");
    print(f"Years of Service: {self.years_of_service}");
    print(f"Missions Completed: {self.missions_completed}");
    print(
        f"Annual Compensation: {format_currency(self.calculate_annual_compensation())}"
    );
}


impl CrewMember.calculate_annual_compensation -> float {
    # Base salary + benefits + mission bonuses
    let base =
        self.salary * 1.10;
    let mission_bonus = self.missions_completed * 2000;
    return base + mission_bonus;
}


impl CrewMember.promote(new_rank: str, salary_increase: float) {
    if self.is_eligible_for_promotion() {
        let old_rank = self.rank;
        self.rank = new_rank;
        self.salary += salary_increase;
        print(f"✓ {self.name} promoted from {old_rank} to {new_rank}");
        print(f"  New salary: {self.salary} + {salary_increase}");
        # Senior ranks get higher clearance
         if self.years_of_service >= SENIOR_CREW_THRESHOLD {
            self.clearance_level = "Advanced";
        }
    } else {
        print(f"✗ {self.name} not eligible for promotion yet.");
        print(f"  Requires {PROMOTION_ELIGIBILITY_YEARS} years of service.");
    }
}


impl CrewMember.grant_bonus(amount: float) {
    print(f"💵 Bonus granted to {self.name}: {amount}");
# In a real system, this would update a bonus field
 }


impl CrewMember.is_senior_crew -> bool {
    return self.years_of_service >= SENIOR_CREW_THRESHOLD
    and self.rank in ["Captain", "Chief Medical Officer", "Senior Engineer", "Senior Pilot"]
    ;
}


impl CrewMember.is_eligible_for_promotion -> bool {
    return self.years_of_service >= PROMOTION_ELIGIBILITY_YEARS;
}


impl CrewMember.complete_mission{
    self.missions_completed += 1;
    print(f"🚀 {self.name} completed mission #{self.missions_completed}");
    # Milestone achievements
     if self.missions_completed % 10 == 0 {
        print(f"   🏆 MILESTONE: {self.missions_completed} missions!");
        self.clearance_level = "Elite";
    }
}
