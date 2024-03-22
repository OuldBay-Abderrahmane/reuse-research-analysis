# reuse-research-analysis

### 1. Common and Different features available for each website

#### Belgium 
2 levels
- 'SellerID', 'SellersStockID', 'Imagefiles',
'LastUpOn', 'Weight', 'Weight_Units','Product_Units', 'Imagefile',
'Initial_Price', 'Latest_Price', 'Initial_Stock', 'Stock_Now',
'Condition', 'Dates_Available', 'Material', 'Technical',
'Collection', 'Price_Change', 'Quantity_Change', 
'Store', 'Language', 'Sold', 'Sold_After', 'material', 'dim',
'quantity_n'

#### French
2 levels
- 'BIM_class', 'location',
'date_published', 'price_initial', 'price_latest', 'price_change',
'imagefiles', 'material_type', 'co2', 'avoided_waste',
'quantity_initial', 'quantity_latest', 'disappeared', 'country', 'sold',
'sold_after', 'city', 'deconstruction', 'state', 'constraints',
'images', 'distance', 'rseSummary', 'promotion',
'source', 'conditioning', 'rate', 'diag_it', 'showroom',
'avoidedWastes', 'trustLevel', 'quantity', 'min_quantity', 'end_date',
'pickup_start_date', 'pickup_end_date', 'deposit_mode',
'object', 'material', 'dim', 'quantity_n'

#### Swiss 
4 levels
- 'Imagefiles','LastUpOn', 'Condition', 'eBKP_H',
       'eBKP_H_EN', 'MateriuumCategory','Material', 'Length', 'Width', 'Height',
       'Diameter', 'Weight', 'Color', 'Energy_Efficiency', 'Availability',
       'FirstPrice', 'PriceOnDemand', 'Quantity', 'Saved',
       'LastUpOn', 'PriceChange', 'Sold', 'SoldAfter', 'Provider',
       'Store', 'ID', 'Country', 'Language', 'Imagefile', 'URL',
       'eBKP_H_Generalized', 'ElementType', 'Price', 'Stock', 'Dimensions',
       'material', 'dim', 'quantity_n'

#### Danish 
2 levels
- 'ID', 'Imagefile','Thickness', 'Thickness_unit', 'Door frame', 'Quantity', 'LastPrice',
        'Saved', 'LastUpOn', 'Hanging', 'Width w/frame', 'Width w/frame_unit',
        'Height w/frame', 'Height w/frame_unit', 'Frame thickness',
        'Frame thickness_unit', 'FirstPrice', 'PriceChange',
        'Rail', 'Old glass', 'With corner band', 'Glass', 'Defective glass',
        'Material', 'Installed before', 'Year of manufacture_unit',
        'For built-in', 'Over rebated', 'With angle hinges', 'Connected',
        'With extender bar', 'Convectors', 'Convectors_unit', 'Suspension bracket', 'With thermostat',
        'Press tested', 'Store'

#### GERMANY 
2 levels
- 'Condition', 'MinAmount',
       'Location', 'Manufacturer', 'Properties', 'FirstPriceNumeric',
       'FirstAvailableNumeric', 'LastPriceNumeric', 'LastAvailableNumeric',
       'LastPrice', 'LastAvailable', 'Sold', 'SoldAfter'

#### UK 
2 levels
- 'Name', 'URL', 'Price', 'Business', 'Category', 'Subcategory',
       'Country', 'Location', 'Description', 'Dimensions', 'Age', 'ItemID',
       'SellerID', 'SellersStockID', 'DateOfListing', 'Imagefiles',
       'LastUpOn'






### 2. Analysis of the market places
### 2.0 Summary of the method









### 3. Combination of all marketplaces


import pandas as pd
import numpy as np

# Assuming swiss.dim and swiss.quantity_n are already defined and applied with eval
swiss.dim = swiss.dim.apply(eval)
swiss.quantity_n = swiss.quantity_n.apply(eval)

swiss['quantity_score'] = swiss['quantity_n'].apply(lambda x: x.get('score', np.nan))
quantity_rows_to_replace = swiss[(swiss['quantity_score'] > 0.5) & (swiss['Quantity'].isna())]

# Replace NaN values in Quantity column with corresponding values from swiss.dim
for index, row in quantity_rows_to_replace.iterrows():
    swiss.at[index, 'Quantity'] = swiss.quantity_n[index]["answer"]  # Assuming Quantity is the first dimension


def extract_first_three_numbers(input_string):
    input_string = input_string["answer"]
    numbers = []
    # Regular expression to find the first three numbers in the string
    matches = re.findall(r'\b\d+\b', input_string)
    # Loop through the matches and convert them to integers
    for match in matches:
        number = int(match)
        # Append the number to the list if it's not already present and the list has less than 3 elements
        if number not in numbers and len(numbers) < 3:
            numbers.append(number)
    # If only one number is available, append its square root to the list until it reaches three numbers
    if len(numbers) == 1:
        square_root = np.sqrt(numbers[0])
        numbers.extend([square_root] * 2)
    # If less than three numbers are available, append NaN until it reaches three numbers
    while len(numbers) < 3:
        numbers.append(np.nan)
    return numbers
# Filter rows where quantity_score is superior to 0.5 and Length, Width, or Height is NaN
dimension_rows_to_replace = swiss[(swiss['quantity_score'] > 0.5) & (swiss[['Length', 'Width', 'Height']].isna().any(axis=1))]

# Replace NaN values in Length, Width, and Height columns with corresponding values from swiss.dim
for index, row in dimension_rows_to_replace.iterrows():
    dimensions = extract_first_three_numbers(swiss.dim[index])
    swiss.at[index, 'Length'] = dimensions[2]
    swiss.at[index, 'Height'] = dimensions[0]
    swiss.at[index, 'Width'] = dimensions[1]
swiss = swiss.drop(columns=['Unnamed: 0.1', 'Unnamed: 0'])

percent_missing = swiss.isnull().sum() * 100 / len(swiss)
missing_value_df = pd.DataFrame({'column_name': swiss.columns,
                                 'percent_missing': percent_missing})
missing_value_df.to_csv("missing_swiss.csv")
