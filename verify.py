import sys

# Constants
DAYS = 7
STAFF = 5
SHIFTS = ['M', 'A', 'N']
MAX_SHIFT = 5
MAX_NIGHT_SHIFT = 2
MAX_CONSECUTIVE_WORKING_DAYS = 3
MIN_DAYS_OFF = 2

def process_input():
    vacation_requests = {}
    schedule_lines = []
    parsing_vacation = False
    parsing_schedule = False

    for line in sys.stdin:
        line = line.strip()
        if line == "Vacation Requirements:":
            parsing_vacation = True
            parsing_schedule = False
            continue
        elif line == "Generated Schedule:":
            parsing_vacation = False
            parsing_schedule = True
            continue

        if parsing_vacation and line.startswith("Staff"):
            parts = line.split(": ")
            staff_id = int(parts[0].split(" ")[1])
            days_off = [int(day) for day in parts[1].split(", ")]
            vacation_requests[staff_id] = days_off
        elif parsing_schedule and line.startswith("Day"):
            schedule_lines.append(line)

    return vacation_requests, schedule_lines

def convert_schedule_lines_to_dict(schedule_lines):
    return {(int(day.split(" ")[1]), int(staff.split(" ")[1]), shift.split(" ")[1]): True 
            for day, staff, shift in [line.split(", ") for line in schedule_lines]}


# Verification and Explanation
def verify_schedule(schedule, vacation_requests):
    shift_count = {staff: 0 for staff in range(STAFF)}
    night_shift_count = {staff: 0 for staff in range(STAFF)}
    consecutive_working_days = {staff: 0 for staff in range(STAFF)}
    days_off_count = {staff: 0 for staff in range(STAFF)}
    shift_coverage = {(day, shift): False for day in range(DAYS) for shift in SHIFTS}
    explanations = []

    for staff in range(STAFF):
        for day in range(DAYS):
            worked_today = any(schedule.get((day, staff, shift), False) for shift in SHIFTS)
            if worked_today:
                shift_count[staff] += 1
                consecutive_working_days[staff] = consecutive_working_days[staff] + 1 if day > 0 and any(schedule.get((day - 1, staff, shift), False) for shift in SHIFTS) else 1
                if 'N' in [shift for shift in SHIFTS if schedule.get((day, staff, shift), False)]:
                    night_shift_count[staff] += 1
            else:
                days_off_count[staff] += 1

    for staff in range(STAFF):
        explanations.append(f"Staff {staff}: {shift_count[staff]} total shifts, {night_shift_count[staff]} night shifts, max consecutive working days: {consecutive_working_days[staff]}, total days off: {days_off_count[staff]}")
        if shift_count[staff] > MAX_SHIFT or night_shift_count[staff] > MAX_NIGHT_SHIFT or consecutive_working_days[staff] > MAX_CONSECUTIVE_WORKING_DAYS or days_off_count[staff] < MIN_DAYS_OFF:
            explanations.append(f"Staff {staff} does not meet all constraints.")
        else:
            explanations.append(f"Staff {staff} meets all constraints.")

    for staff, days_off in vacation_requests.items():
        for day in days_off:
            if any(schedule.get((day, staff, shift), False) for shift in SHIFTS):
                explanations.append(f"Violation: Staff {staff} was scheduled on a requested day off: Day {day}.")
            else:
                explanations.append(f"Staff {staff}'s vacation request for Day {day} is honored.")

    # Detailed Shift Coverage
    shift_coverage_detail = {day: {shift: [] for shift in SHIFTS} for day in range(DAYS)}

    for day in range(DAYS):
        for shift in SHIFTS:
            for staff in range(STAFF):
                if schedule.get((day, staff, shift), False):
                    shift_coverage_detail[day][shift].append(f"Staff {staff}")
    # Formatting and Adding Shift Coverage Details to Explanations
    explanations.append("Detailed Shift Coverage:")
    for day in range(DAYS):
        explanations.append(f"  Day {day}:")
        for shift in SHIFTS:
            staff_assigned = ', '.join(shift_coverage_detail[day][shift])
            if staff_assigned:
                explanations.append(f"    Shift {shift}: {staff_assigned}")
            else:
                explanations.append(f"    Shift {shift}: No staff assigned (Uncovered)")
    # Update shift_coverage based on shift_coverage_detail
    for day in range(DAYS):
        for shift in SHIFTS:
            staff_assigned = shift_coverage_detail[day][shift]
            if staff_assigned:
                shift_coverage[(day, shift)] = True                

    uncovered_shifts = [(day, shift) for (day, shift), covered in shift_coverage.items() if not covered]
    if uncovered_shifts:
        explanations.append(f"Uncovered shifts: {uncovered_shifts}")
    else:
        explanations.append("All shifts are covered.")
    all_constraints_satisfied = all(shift_count[staff] <= MAX_SHIFT and night_shift_count[staff] <= MAX_NIGHT_SHIFT and consecutive_working_days[staff] <= MAX_CONSECUTIVE_WORKING_DAYS and days_off_count[staff ] >= MIN_DAYS_OFF for staff in range(STAFF)) and not uncovered_shifts
    if all_constraints_satisfied:
        explanations.append("Overall, the schedule satisfies all constraints and vacation requests.")
    else:
        explanations.append("The schedule does not satisfy all constraints and/or vacation requests.")

    return "\n".join(explanations)

# Main execution
def main():
    vacation_requests, schedule_lines = process_input()
    schedule = convert_schedule_lines_to_dict(schedule_lines)
    result = verify_schedule(schedule, vacation_requests)
    print(result)

if __name__ == "__main__":
    main()