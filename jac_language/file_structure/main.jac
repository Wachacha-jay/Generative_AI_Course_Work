"""
Space Station Crew Management System
Main program entry point
"""

import from models.employee { Employee, CrewMember }
import from utils.helpers { print_header, calculate_bonus }
import from utils.constants { STATION_NAME, DEPARTMENTS }


with entry:__main__ {
    print_header("Welcome to " + STATION_NAME);
    # Create crew members
    let captain =
        CrewMember(
            id="EMP001",
            name="Commander Sarah Chen",
            department="Command",
            rank="Captain",
            salary=125000,
            years_of_service=12
        );
    let engineer =
        CrewMember(
            id="EMP002",
            name="Tech Specialist Marcus Rodriguez",
            department="Engineering",
            rank="Senior Engineer",
            salary=95000,
            years_of_service=8
        );
    let medic =
        CrewMember(
            id="EMP003",
            name="Dr. Yuki Tanaka",
            department="Medical",
            rank="Chief Medical Officer",
            salary=110000,
            years_of_service=10
        );
    let pilot =
        CrewMember(
            id="EMP004",
            name="Lieutenant Alex Volkov",
            department="Navigation",
            rank="Pilot",
            salary=78000,
            years_of_service=4
        );
    # Add crew to station roster
    let crew_roster =
        [captain, engineer, medic, pilot];
    print("\n=== CREW ROSTER ===");
    for member in crew_roster {
        member.display_info();
        print("");
    }
    # Perform crew operations
    print(
        "\n=== CREW OPERATIONS ==="
    );
    # Promote the pilot
    print(
        "🚀 Promotion Event:"
    );
    pilot.promote("Senior Pilot", 15000);
    # Grant mission bonus
    print(
        "\n💰 Mission Completion Bonuses:"
    );
    for member in crew_roster {
        let bonus = calculate_bonus(member.salary, member.years_of_service);
        member.grant_bonus(bonus);
    }
    # Display station statistics
    print(
        "\n=== STATION STATISTICS ==="
    );
    let total_payroll: int = 0;
    let avg_service: float = 0.0;
    for member in crew_roster {
        total_payroll += member.salary;
        avg_service += member.years_of_service;
    }
    avg_service = avg_service / len(crew_roster);
    print(f"Total Crew Members: {len(crew_roster)}");
    print(f"Total Annual Payroll: {total_payroll}");
    print(f"Average Years of Service: {avg_service} years");
    print("\n=== DEPARTMENT BREAKDOWN ===");
    for dept in DEPARTMENTS {
        let dept_count = 0;
        for member in crew_roster {
            if member.department == dept {
                dept_count += 1;
            }
        }
        print(f"{dept}: {dept_count} crew member(s)");
    }
    # Test senior crew eligibility
    print(
        "\n=== SENIOR CREW STATUS ==="
    );
    for member in crew_roster {
        let status = "✓ Eligible" if member.is_senior_crew() else "✗ Not eligible";
        print(f"{member.name}: {status}");
    }
    print_header("End of Shift Report");
}
