"""
Application Constants
Configuration values and constants for the crew management system
"""

# Station Information
 glob STATION_NAME = "ISS-Artemis Orbital Platform";
glob STATION_CAPACITY = 50;
glob STATION_ESTABLISHED = 2030;

# Department Definitions
 glob DEPARTMENTS =

    ["Command",
    "Engineering",
    "Medical",
    "Navigation",
    "Science",
    "Operations",
    "Security",
    "Communications"];

# Rank Hierarchy (lowest to highest)
 glob RANKS =

    ["Cadet",
    "Crew Member",
    "Specialist",
    "Senior Specialist",
    "Officer",
    "Senior Officer",
    "Department Head",
    "Commander",
    "Captain"];

# Salary Ranges by Rank (annual in USD)
 glob SALARY_RANGES =

    {"Cadet" : (45000, 55000) , "Crew Member" : (60000, 75000) , "Specialist" : (75000, 90000) , "Senior Specialist" : (90000, 110000) , "Officer" : (100000, 120000) , "Senior Officer" : (115000, 135000) , "Department Head" : (130000, 150000) , "Commander" : (145000, 165000) , "Captain" : (160000, 200000) };

# Employment Thresholds
 glob PROBATION_PERIOD = 1;
# years
 glob PROMOTION_ELIGIBILITY_YEARS = 3;
# minimum years for promotion
 glob SENIOR_CREW_THRESHOLD = 8;
# years to be considered senior crew
 glob VETERAN_THRESHOLD = 15;
# years to be considered veteran
 glob RETIREMENT_YEARS = 30;
# years until retirement eligibility
 # Compensation & Benefits
 glob BONUS_BASE_RATE = 0.08;
# 8% of salary
 glob SENIOR_BONUS_MULTIPLIER = 1.5;
# 50% bonus increase for senior crew
 glob BENEFITS_PERCENTAGE = 0.10;
# 10% of salary for benefits
 glob MISSION_BONUS = 2000;
# bonus per mission completed
 # Clearance Levels
 glob CLEARANCE_LEVELS =
    ["Standard", "Advanced", "Elite", "Classified"];

# Mission Types
 glob MISSION_TYPES =

    ["Routine Maintenance",
    "Scientific Research",
    "External Repair",
    "Supply Transfer",
    "Emergency Response",
    "Deep Space Exploration"];

# Performance Metrics
 glob MIN_PERFORMANCE_SCORE = 0;
glob MAX_PERFORMANCE_SCORE = 100;
glob EXCELLENT_PERFORMANCE = 90;
glob GOOD_PERFORMANCE = 75;
glob SATISFACTORY_PERFORMANCE = 60;

# System Configuration
 glob MAX_CREW_PER_DEPARTMENT = 10;
glob SHIFT_HOURS = 8;
glob SHIFTS_PER_DAY = 3;
glob VACATION_DAYS_PER_YEAR = 30;
glob SICK_DAYS_PER_YEAR = 15;

# Emergency Protocols
 glob EMERGENCY_STATIONS =

    {"Command" : "Bridge Alpha" , "Engineering" : "Engineering Bay" , "Medical" : "MedBay Primary" , "Navigation" : "Navigation Hub" , "Science" : "Laboratory Sector" , "Operations" : "Operations Center" , "Security" : "Security Station" , "Communications" : "ComHub Central" };

# Training Requirements (hours per year)
 glob REQUIRED_TRAINING_HOURS =
    {"Safety" : 40 , "Technical" : 60 , "Leadership" : 20 , "Emergency" : 30 };

# Application Metadata
 glob APP_VERSION = "2.1.0";
glob APP_NAME = "Crew Management System";
glob DEVELOPER = "Space Operations Division";
glob LAST_UPDATED = "2025-10-02";
