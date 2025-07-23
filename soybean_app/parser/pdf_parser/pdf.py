#Pulling data out of John Deere PDF's
#library: PDFPlumber

import re
import pdfplumber
import json
import shutil
from pathlib import Path
from save_to_csv import save_to_csv

#TODO: setup folder to pull uploads from, not just static location
#TODO: extract into dataframe to be put in a db? -- talk to Dr. Lee about this
#TODO:/NTS tweak regex patterns later to not include measurements, just numbers. some kept for now just for readability, but cannot assign "4.3 gallons" as an integer when we export this


#temp location to make sure it works
loc = r"C:\Users\jsimp\OneDrive\Documents\GitHub\Applied-Data-Science-in-Crop-Analytics\soybean_app\data\sample_uploads\Northwest Hill Overview Seeding (2).pdf"

# Folder paths
RAW_DIR = Path("soybean_app/data/raw")
DISCARDS_DIR = Path("soybean_app/data/raw_discards")

#print all text to console
def dump(text):
    print(text)

def extract_farm_data(text):
    # keys, regex pattern
    patterns = {
    "fieldName": r"Field:\s*(.+?)\s*(?:UCM Farms|\|)",
    "startTime": r"Start:\s*(.+?)\sEnd:",
    "endTime": r"End:\s*(.+?)\sWork Totals",
    "areaSeeded": r"Area Seeded:\s*([\d.]+)",
    "appliedRate": r"Applied Rate:\s*([\d,]+)",
    "appliedTotal": r"Applied Total:\s*([\d,]+)",
    "targetRate": r"Target Rate:\s*([\d,]+)",
    "targetTotal": r"Target Total:\s*([\d,]+)",
    "seedingTime": r"Seeding Time:\s*([\dhm\s]+)",
    "speed": r"Speed:\s*([\d.]+)",
    "productivity": r"Productivity:\s*([\d.]+)",
    "totalFuel": r"Total Fuel:\s*([\d.]+)",
    "fuelRateArea": r"Fuel Rate \(Area\):\s*([\d.]+)",
    "fuelRateTime": r"Fuel Rate \(Time\):\s*([\d.]+)",
    "equipmentSerial": r"Equipment\s+(.+?):",
    "seedVariety": r"Varieties\s+(\d+)",
    }

    #build our dictionary with pattern name as key and default value as None
    extracted_data: dict[str, str | None] = {key: None for key in patterns}

    #loop through patterns, pull data if applicable
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            extracted_data[key] = match.group(1).strip()

    return extracted_data


#display cleaned data
def print_extracted_data(data):
            
            if data is None:
                 print("No data was returned!")
            else:
                for key, value in data.items():
                    print(f"{key}: {value}")
            


def process_pdf_file(pdf_path: Path):
    with pdfplumber.open(pdf_path) as pdf:
        text = pdf.pages[0].extract_text().replace('\n', ' ')
        extracted = extract_farm_data(text)

    # Save data to CSV
    save_to_csv(extracted)

    # create our discard subfolder for the newly processed pdf
    discard_folder = DISCARDS_DIR / pdf_path.stem
    discard_folder.mkdir(parents=True, exist_ok=True)

    # Save extracted data as JSON
    json_path = discard_folder / f"{pdf_path.stem}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(extracted, f, indent=2)

    # Move the original PDF to its discard subfolder
    shutil.move(str(pdf_path), str(discard_folder / pdf_path.name))

    print(f"Processed and archived: {pdf_path.name}")


def main():
    pdf_files = list(RAW_DIR.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files currently found in raw/.")
        return

    for pdf_path in pdf_files:
        try:
            process_pdf_file(pdf_path)
        except Exception as e:
            print(f"unable to process {pdf_path.name}: {e}")


if __name__ == "__main__":
    main()
