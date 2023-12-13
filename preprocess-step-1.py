import pandas as pd

# Path to the Excel file inside the 'data' folder
file_path = 'data/House_Pricing.xls'

# Load the first sheet of the Excel file
sheet1_df = pd.read_excel(file_path, sheet_name=0)

# Filtering out rows with NaN values
filtered_df = sheet1_df.dropna().reset_index(drop=True)

# Adjusted approach: Extract series IDs and titles, considering the next row after 'Series ID:' and 'Title:'
series_id_list = []
title_list = []
basic_category_list = []
broad_category_list = []

for index in range(len(filtered_df) - 1):
    if 'Series ID:' in filtered_df.iloc[index]['Data List: House Pricing']:
        series_id = filtered_df.iloc[index + 1]['Data List: House Pricing']
        series_id_list.append(series_id)
    elif 'Title:' in filtered_df.iloc[index]['Data List: House Pricing']:
        title = filtered_df.iloc[index + 1]['Data List: House Pricing']
        title_list.append(title)
        
        # Basic Category
        # Broad Category
        category_type= ["Construction", "Purchasing Power", "Target", "Rent Price", "Advertising"]
        basic_category = None
        broad_category = None
        if "Home Price Index" in title:
            basic_category = "Target"
            broad_category = "Target"
        elif "Rent" in title:
            basic_category = "Rent"
            broad_category = "Rent"
        elif "Purchasing" in title:
            basic_category = "Purchasing"
            broad_category = "Purchasing"
        elif "Advertising" in title:
            basic_category = "Advertising"
            broad_category = "Construction"
        elif "Transportation":
            basic_category = "Transportation"
            broad_category = "Construction"           
        elif "Producer" in title or "Consumer" in title:
            basic_category = "Construction"
            broad_category = "Construction"
                
        basic_category_list.append(basic_category)
        broad_category_list.append(broad_category)


# Creating a DataFrame for the series IDs and their corresponding titles
corrected_series_titles_df = pd.DataFrame({'Series ID': series_id_list, 'Title': title_list, "Basic Category": basic_category_list, "Broad Category": broad_category_list})
corrected_series_titles_df.to_csv('data/Categories.csv', index=False, encoding='utf-8')
# print(corrected_series_titles_df.head())
