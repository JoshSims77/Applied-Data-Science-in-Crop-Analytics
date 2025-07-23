import csv
import os


COLUMNS = [
    "fieldName", "startTime", "endTime",
    "areaSeeded", "appliedRate", "appliedTotal",
    "targetRate", "targetTotal", "seedingTime",
    "speed", "productivity", "totalFuel",
    "fuelRateArea", "fuelRateTime",
    "equipmentSerial", "seedVariety"
]


CSV_PATH = "soybean_app/data/processed/soybean_data.csv"

def save_to_csv(data_dict, filepath=CSV_PATH):
    file_exists = os.path.isfile(filepath)

    with open(filepath, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=COLUMNS)

        if not file_exists:
            writer.writeheader()  # Write headers only once
            
        safe_data = {key: (data_dict.get(key) or "") for key in COLUMNS}
        writer.writerow(data_dict)
