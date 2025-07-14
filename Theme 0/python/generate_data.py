import os
import csv
import random
from datetime import datetime, timedelta

# --- Configuration ---
NUM_VARIANTS = 10
RECORDS_PER_FILE = 100
START_DATE = datetime(2025, 6, 1)
END_DATE = datetime(2025, 7, 10)

REGIONS = ["Північ", "Схід", "Південь", "Захід", "Центр"]
INCIDENT_TYPES = ["Кібератака", "Логістичний збій", "Технічна несправність", "Діяльність ДРГ", "Порушення зв'язку"]
PRIORITIES = ["Низький", "Середній", "Високий", "Критичний"]
BASE_DIR = "final_assessment"

# --- Data Generation Logic ---
def create_random_date(start, end):
    """Generates a random date between two dates."""
    delta = end - start
    random_days = random.randrange(delta.days)
    return start + timedelta(days=random_days)

def generate_data(filename, num_records):
    """Generates a CSV file with random incident data."""
    header = ["date", "region", "incident_type", "priority", "personnel_involved"]
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for _ in range(num_records):
            region = random.choices(REGIONS, weights=[0.2, 0.3, 0.2, 0.1, 0.2], k=1)[0]
            incident = random.choices(INCIDENT_TYPES, weights=[0.3, 0.1, 0.2, 0.2, 0.2], k=1)[0]
            writer.writerow([
                create_random_date(START_DATE, END_DATE).strftime('%Y-%m-%d'),
                region,
                incident,
                random.choice(PRIORITIES),
                random.randint(1, 25)
            ])

# --- Main Execution ---
if __name__ == "__main__":
    # Create base directory if it doesn't exist
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)

    # Create variant folders and data files
    for i in range(1, NUM_VARIANTS + 1):
        variant_folder = os.path.join(BASE_DIR, f"variant_{i:02d}")
        if not os.path.exists(variant_folder):
            os.makedirs(variant_folder)
        
        output_file = os.path.join(variant_folder, "incident_reports.csv")
        # Add some variability to the number of records for each variant
        generate_data(output_file, RECORDS_PER_FILE + random.randint(-20, 20))
    
    print(f"Successfully generated {NUM_VARIANTS} variants in '{BASE_DIR}' directory.")