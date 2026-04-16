import csv


# 1. FUNCTION ADDED
def clean_row(row):
    """
    Clean and normalize a single survey row.

    This function:
    - normalizes role names to title case
    - converts satisfaction_score to an integer when possible
    - converts experience_years to an integer when possible
    - replaces missing participant names with "Unknown"
    """
    cleaned = row.copy()

    # FIX: Handle missing participant names (R005 was blank)
    name = cleaned.get("participant_name", "").strip()
    cleaned["participant_name"] = name if name else "Unknown"

    # FIX: Normalize inconsistent capitalization (e.g., "ux researcher" → "Ux Researcher")
    cleaned["role"] = cleaned.get("role", "").strip().title()
    cleaned["department"] = cleaned.get("department", "").strip().title()
    cleaned["primary_tool"] = cleaned.get("primary_tool", "").strip().title()

    # FIX: Prevent crashes when satisfaction_score is missing or invalid
    satisfaction = cleaned.get("satisfaction_score", "").strip()
    if satisfaction.isdigit():
        cleaned["satisfaction_score"] = int(satisfaction)
    else:
        cleaned["satisfaction_score"] = None

    # FIX: Prevent crash from invalid data like "fifteen" in experience_years (R009)
    experience = cleaned.get("experience_years", "").strip()
    if experience.isdigit():
        cleaned["experience_years"] = int(experience)
    else:
        cleaned["experience_years"] = None

    return cleaned


# Load the survey data from a CSV file
filename = "week3_survey_messy.csv"
rows = []

with open(filename, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    
    # FIX: Previously missing body → caused error and rows never filled
    for row in reader:
        cleaned = clean_row(row)   # FIX: Clean each row before using it
        rows.append(cleaned)       # FIX: Actually append rows (was missing entirely)


# Count responses by role
role_counts = {}

for row in rows:
    role = row["role"]
    
    # FIX: Skip empty roles (from missing data)
    if role:
        if role in role_counts:
            role_counts[role] += 1
        else:
            role_counts[role] = 1

print("Responses by role:")
for role, count in sorted(role_counts.items()):
    print(f"  {role}: {count}")


# Calculate the average years of experience
total_experience = 0
valid_experience_count = 0

for row in rows:
    # FIX: Only include valid numeric values (avoids crash from "fifteen")
    if row["experience_years"] is not None:
        total_experience += row["experience_years"]
        valid_experience_count += 1

# FIX: Avoid division by zero if all values were invalid
if valid_experience_count > 0:
    avg_experience = total_experience / valid_experience_count
    print(f"\nAverage years of experience: {avg_experience:.1f}")
else:
    print("\nAverage years of experience: No valid data")


# Find the top 5 highest satisfaction scores
scored_rows = []

for row in rows:
    # FIX: Only include valid numeric satisfaction scores
    if row["satisfaction_score"] is not None:
        scored_rows.append((row["participant_name"], row["satisfaction_score"]))

# FIX: Previously sorted ascending (LOWEST first) → now highest first
scored_rows.sort(key=lambda x: x[1], reverse=True)
top5 = scored_rows[:5]

print("\nTop 5 highest satisfaction scores:")
for name, score in top5:
    print(f"  {name}: {score}")


# 2. WRITE CLEANED DATA TO A NEW CSV FILE
output_filename = "week3_survey_cleaned.csv"

fieldnames = [
    "response_id",
    "participant_name",
    "role",
    "department",
    "age_range",
    "experience_years",
    "satisfaction_score",
    "primary_tool",
    "response_text",
]

with open(output_filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for row in rows:
        output_row = row.copy()

        # FIX: Convert None back to blank for CSV output
        if output_row["experience_years"] is None:
            output_row["experience_years"] = ""
        if output_row["satisfaction_score"] is None:
            output_row["satisfaction_score"] = ""

        writer.writerow(output_row)

print(f"\nCleaned data written to {output_filename}")