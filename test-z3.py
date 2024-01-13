from z3 import *

# Constants
DAYS = 7
STAFF = 5
SHIFTS = ['M', 'A', 'N']
MAX_CONSECUTIVE_WORKING_DAYS = 3
MIN_DAYS_OFF = 2

# Example vacation requests
vacation_requests = {
    0: [0, 1, 5],  # Staff 0 requested days 1 and 5 off
    1: [0, 1, 5,2,3,4, 6],  # Staff 0 requested days 1 and 5 off
    3: [0, 1, 5,2,3,4],  # Staff 0 requested days 1 and 5 off
    # 4: [0, 1, 5,2,3,4],  # Staff 0 requested days 1 and 5 off
    2: [3],     # Staff 2 requested day 3 off
    # Add more requests as needed
}

# Create a solver instance
s = Solver()

# Schedule variable: 3D array of Bool (day, staff, shift)
schedule = [[[Bool(f"day_{d}_staff_{p}_shift_{s}") for s in SHIFTS] for p in range(STAFF)] for d in range(DAYS)]
# Calculate the flattened length of the schedule array
flattened_length = sum(len(schedule[d][p]) for d in range(DAYS) for p in range(STAFF))

# Adding constraints
for p in range(STAFF):
    # Maximum total shifts constraint
    # Add a constraint to the solver
    s.add(
        # Calculate the sum of shifts worked by a staff member over the specified days
        Sum([
            # If the condition (shift is assigned) is true, return 1, otherwise return 0
            If(
                # Check if any shift is assigned for a particular day and staff member
                Or(schedule[d][p]),  
                1,  # If a shift is assigned, count it as 1
                0   # If no shift is assigned, count it as 0
            )
            # Iterate through the range of days (0 to DAYS-1)
            for d in range(DAYS)
        ])
        # Ensure that the sum of shifts worked by the staff member is less than or equal to 5
        <= 5
    )


    # Maximum night shifts constraint
    s.add(Sum([If(schedule[d][p][2], 1, 0) for d in range(DAYS)]) <= 2)

    # Maximum consecutive working days constraint
    for d in range(DAYS - MAX_CONSECUTIVE_WORKING_DAYS):
        s.add(Sum([If(Or(schedule[d+i][p]), 1, 0) for i in range(MAX_CONSECUTIVE_WORKING_DAYS + 1)]) <= MAX_CONSECUTIVE_WORKING_DAYS)

    # Mandatory days off constraint
    s.add(Sum([If(Or(schedule[d][p]), 0, 1) for d in range(DAYS)]) >= MIN_DAYS_OFF)

    # Vacation requests constraint
    for day_off in vacation_requests.get(p, []):
        s.add(Not(Or(schedule[day_off][p])))

# Constraint: Ensure all shifts are covered each day
for d in range(DAYS):
    for shift_index in range(len(SHIFTS)):
        s.add(Or([schedule[d][p][shift_index] for p in range(STAFF)]))  # At least one staff per shift each day



# Solve the scheduling problem
if s.check() == sat:
    m = s.model()

    # Print the vacation requirements
    print("Vacation Requirements:")
    for staff, days_off in vacation_requests.items():
        days_off_str = ", ".join(map(str, days_off))
        print(f"Staff {staff} requested days off: {days_off_str}")

    # Print the generated schedule
    print("\nGenerated Schedule:")
    for d in range(DAYS):
        for p in range(STAFF):
            for shift_index, shift_name in enumerate(SHIFTS):
                if is_true(m.evaluate(schedule[d][p][shift_index])):
                    print(f"Day {d}, Staff {p}, Shift {shift_name}")
else:
    print(s.unsat_core())
    print("No solution found")
