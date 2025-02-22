import csv
import json
import sys


if len(sys.argv) < 3:
    print("Usage: python json_to_csv.py input.json output.csv")
    sys.exit(1)
input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)
if isinstance(data, dict):
    data = [data]
fieldnames = data[0].keys()

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

print(f"CSV file '{output_file}' has been created successfully.")
