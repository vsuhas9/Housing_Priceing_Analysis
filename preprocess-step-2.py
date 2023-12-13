import pandas as pd
import numpy as np

# Load the Categories.csv file
categories_df = pd.read_csv('data/Categories.csv')

# Load the second sheet from the House_Pricing.xls file
house_pricing_df = pd.read_excel('data/House_Pricing.xls', sheet_name=1)

# Create a mapping of series names to broad categories
series_to_category_map = dict(
    zip(categories_df['Series ID'], categories_df['Broad Category']))

# Update the mapping to include only series names present in the house pricing data
updated_series_to_category_map = {
    k: v for k, v in series_to_category_map.items() if k in house_pricing_df.columns}


# Re-defining the file paths for the US GDP and US Inflation files
gdp_file_path = 'data/US GDP.csv'
inflation_file_path = 'data/US inflation.csv'
immigration_file_path = 'data/US immigration.csv'

# Loading the US GDP and US Inflation data
gdp_df = pd.read_csv(gdp_file_path)
inflation_df = pd.read_csv(inflation_file_path)
immigration_df = pd.read_csv(immigration_file_path)

# Extracting the year and the required columns ('Per Capita (US $)' and 'Inflation Rate (%)')
per_capita_income_list = list(gdp_df[' Per Capita (US $)'])
inflation_rate_list = list(inflation_df[' Inflation Rate (%)'])
immigration_df['Refugee Arrivals'] = immigration_df['Refugee Arrivals'].str.replace(
    ',', '').astype(int)
immigration_df['Noncitizen Apprehensions'] = immigration_df['Noncitizen Apprehensions'].str.replace(
    ',', '').astype(int)
immigration_list = list(
    immigration_df['Refugee Arrivals'] + immigration_df['Noncitizen Apprehensions'])

# print(len(per_capita_income_list), len(
#    inflation_rate_list), len(immigration_list))

per_capita_final = []
immigration_final = []
inflation_final = []

for year in range(len(immigration_list)-1):
    for each_month in range(1, 13):
        per_capita_final.append(
            each_month*((per_capita_income_list[year] + per_capita_income_list[year+1])/12))
        immigration_final.append(
            each_month*((immigration_list[year] + immigration_list[year+1])/12))
        inflation_final.append(
            each_month*((inflation_rate_list[year] + inflation_rate_list[year+1])/12))
        # print(inflation_rate_list[year], year+2000, "-", each_month)

for mon in range(9):
    inflation_final.append(np.nan)
    immigration_final.append(np.nan)
    per_capita_final.append(np.nan)

print(len(house_pricing_df['DATE']), len(per_capita_final), len(
    immigration_final), len(inflation_final))


# Initialize a dictionary to hold the summed values for each broad category
summed_data = {"DATE": house_pricing_df['DATE'], "Per Capita": per_capita_final,
               "Immigration Count": immigration_final, "Inflation": inflation_final}

# print(type(house_pricing_df['DATE']))

# Summing columns for each broad category using the updated mapping
for category in categories_df['Broad Category'].unique():
    category_columns = [col for col in house_pricing_df.columns
                        if updated_series_to_category_map.get(col, None) == category]
    if category_columns:
        summed_data[category] = house_pricing_df[category_columns].sum(
            axis=1, skipna=False)


summed_df = pd.DataFrame(summed_data)
# Remove rows with NaN values
cleaned_summed_df = summed_df.dropna()


# Extract the column you want to move
column_to_move = cleaned_summed_df.pop('Target')


# Reinsert the column at the end
cleaned_summed_df['Target'] = column_to_move

# Save the cleaned DataFrame as a CSV file
csv_output_path = 'Clean_House_Pricing_Index.csv'
cleaned_summed_df.to_csv(csv_output_path, index=False)
