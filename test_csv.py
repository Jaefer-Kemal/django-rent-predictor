import pandas as pd
import random

# Parameters for generating data
neighborhoods = ['A', 'B', 'C', 'D']
conditions = ['New', 'Good', 'Average']
size_range = (1200, 3500)
distance_range = (1, 30)

# Initialize list to store data rows
data = []

# Generate 300 rows
for _ in range(300):
    size = random.randint(*size_range)
    bedrooms = max(1, size // 700)
    bathrooms = max(1, size // 1000)
    neighborhood = random.choice(neighborhoods)
    condition = random.choice(conditions)
    distance = round(random.uniform(*distance_range), 1)
    
    # Base price calculations
    base_price = size * 100
    
    # Adjust based on neighborhood
    if neighborhood == 'A':
        base_price *= 1.5
    elif neighborhood == 'B':
        base_price *= 1.2
    elif neighborhood == 'C':
        base_price *= 0.9
    elif neighborhood == 'D':
        base_price *= 0.7
    
    # Adjust based on condition
    if condition == 'New':
        base_price *= 1.5
    elif condition == 'Good':
        base_price *= 1.1
    elif condition == 'Average':
        base_price *= 0.9
    
    # Adjust based on distance
    price = int(base_price / (distance ** 0.5))   
    
    # Append the row
    data.append([size, bedrooms, bathrooms, neighborhood, condition, distance, price])

# Create DataFrame and save to CSV
df = pd.DataFrame(data, columns=[
    'Size (sq ft)', 'Bedrooms', 'Bathrooms', 'Neighborhood', 'Condition', 'Distance to City Center (km)', 'Rent Price (ETB)'
])

df.to_csv('housing_rent_data_300.csv', index=False)
