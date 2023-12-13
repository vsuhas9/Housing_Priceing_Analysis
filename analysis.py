# Since the code execution environment currently supports Python, I will continue with Python for the analysis.
# However, I'll make sure to use methodologies and approaches that are easily translatable to R.

import pandas as pd
import seaborn as sns
from datetime import datetime
import matplotlib.pyplot as plt

# Setting the style for the plots
sns.set(style="whitegrid")

data = pd.read_csv("Clean_House_Pricing_Index.csv")

# Plotting each feature over time
features = ['Per Capita', 'Immigration Count',
            'Inflation', 'Construction', 'Purchasing', 'Rent']
plt.figure(figsize=(15, 10))

data_reset = data.reset_index()

dates = [datetime.strptime(date, "%Y-%m-%d") for date in list(data['DATE'])]

for i, feature in enumerate(features, 1):
    plt.subplot(3, 2, i)
    plt.plot(dates, data[feature], label=feature)
    plt.xlabel('Date')
    if feature == "Purchasing":
        feature = "Purchasing Power "
    plt.ylabel(feature + " Index")
    plt.title(f'{feature} Over Time')
    plt.xticks(rotation=45)

plt.tight_layout()
# plt.show()
plt.savefig('Visualizing Inputs.pdf')

# Calculating the correlation matrix
data_corr = data[features]
correlation_matrix = data_corr.corr()

# Plotting the correlation matrix
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Matrix")
plt.savefig('Correlation Analysis.pdf')
