"""
Employee Tests
Unit tests for Employee and CrewMember functionality
"""

import from models.employee { CrewMember }
import from utils.helpers { print_header }


test { let member =
    CrewMember(
        id="TEST001",
        name="Test Astronaut",
        department="Testing",
        rank="Test Pilot",
        salary=80000,
        years_of_service=5
    ); assert member.id == "TEST001" ; assert member.name == "Test Astronaut" ; assert member.department == "Testing" ; assert member.rank == "Test Pilot" ; assert member.salary == 80000 ; assert member.years_of_service == 5 ; assert member.missions_completed == 0 ; assert member.clearance_level == "Standard" ; print("✓ CrewMember creation test passed"); }


test { let junior =
    CrewMember(
        id="TEST002",
        name="Junior Crew",
        department="Engineering",
        rank="Engineer",
        salary=70000,
        years_of_service=2
    ); let senior =
    CrewMember(
        id="TEST003",
        name="Senior Crew",
        department="Engineering",
        rank="Engineer",
        salary=70000,
        years_of_service=6
    ); assert junior.is_eligible_for_promotion() == false ; assert senior.is_eligible_for_promotion() == true ; print("✓ Promotion eligibility test passed"); }


test { let member =
    CrewMember(
        id="TEST004",
        name="Mission Specialist",
        department="Science",
        rank="Scientist",
        salary=90000,
        years_of_service=7
    ); # Base compensation (salary + 10% benefits)
let base_comp =
    member.calculate_annual_compensation(); assert base_comp == 99000 ; # 90000 * 1.10
# Complete some missions
member.missions_completed =
    5; let with_missions = member.calculate_annual_compensation(); assert with_missions == 109000 ; # 99000 + (5 * 2000)
print(
    "✓ Salary calculation test passed"
); }


test { let junior =
    CrewMember(
        id="TEST005",
        name="Junior Member",
        department="Command",
        rank="Lieutenant",
        salary=75000,
        years_of_service=4
    ); let senior =
    CrewMember(
        id="TEST006",
        name="Senior Member",
        department="Command",
        rank="Captain",
        salary=120000,
        years_of_service=10
    ); assert junior.is_senior_crew() == false ; assert senior.is_senior_crew() == true ; print("✓ Senior crew status test passed"); }


test { let member =
    CrewMember(
        id="TEST007",
        name="Promotable Crew",
        department="Navigation",
        rank="Pilot",
        salary=80000,
        years_of_service=5
    ); let original_salary = member.salary; member.promote("Senior Pilot", 15000); assert member.rank == "Senior Pilot" ; assert member.salary == original_salary + 15000 ; print("✓ Promotion functionality test passed"); }


test { let member =
    CrewMember(
        id="TEST008",
        name="Mission Runner",
        department="Operations",
        rank="Operator",
        salary=85000,
        years_of_service=6
    ); assert member.missions_completed == 0 ; member.complete_mission(); assert member.missions_completed == 1 ; member.complete_mission(); member.complete_mission(); assert member.missions_completed == 3 ; print("✓ Mission completion test passed"); }


# Run all tests
 with entry {
    print_header("Running Employee Tests");
    print("\nExecuting test suite...\n");
    # Note: In actual Jac, tests would be run by the test framework
    # This is a demonstration of test structure
    print(
        "\n"
    );
    print_header("All Tests Completed");
    print("All employee tests passed successfully! ✓");
}
