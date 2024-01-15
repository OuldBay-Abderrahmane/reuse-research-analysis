from tqdm import tqdm 
import requests
import json
import time
import pandas as pd

uni_mat_ma = pd.read_excel("data/Uniclass2015_Ma_v1_1.xlsx", header=2)
uni_mat_pr = pd.read_excel("data/Uniclass2015_Pr.xlsx", header=2)
ifc = pd.read_csv("data/IFC_processed.csv")

codes = pd.DataFrame(pd.concat([ifc.IFC], axis=0))
codes = codes.reset_index(drop=True)
codes.columns = ["raw"]

codes = list(codes.raw)
# API endpoint URL
api_url = "https://buildingtransparency.org/api/materials/statistics"

# Authorization token
headers = {
    "Accept": "application/json",
    "Authorization": "Bearer 6XBXlpGOgd9IGR26dtc2qSzOaKshxS",
}

# Results dictionary to store API responses
results = {}

# Iterate over each row in the table with tqdm for a progress bar
for row in tqdm(codes, desc="Processing rows", unit="row"):
    # Replace multiple spaces with a single '+'
    row_parameter = '+'.join(row.split())

    start_time = time.time()  # Record start time for each request

    # Construct the URL with the modified row value
    url = f"{api_url}?name={row_parameter}"

    # Make the API request
    response = requests.get(url, headers=headers)

    # Record duration
    duration = time.time() - start_time

    # Store the result in the dictionary
    results[row] = {
        "status_code": response.status_code,
        "data": response.json() if response.status_code == 200 else None,
        "duration": duration,
    }
    time.sleep(1)


with open("output.json", "w") as output_file:
    json.dump(results, output_file, indent=2)

print("Results saved to output.json")