import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import os 
import plotly.express as px
import matplotlib
matplotlib.use('Agg')

def train_model(file_path):
    # Load the new CSV file
    housing_data = pd.read_csv(file_path)
    
    # Process data
    housing_data = pd.get_dummies(housing_data, columns=['Neighborhood', 'Condition'], drop_first=True)
    X = housing_data.drop(columns=['Rent Price (ETB)'])
    y = housing_data['Rent Price (ETB)']

    # Scale the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train the model
    lr_model = LinearRegression()
    lr_model.fit(X_scaled, y)

    # Save model and scaler
    joblib.dump(lr_model, 'lr_model.pkl')
    joblib.dump(scaler, 'scaler.pkl')

def predict_rent(input_data):
    
    # Load trained model and scaler
    lr_model = joblib.load('lr_model.pkl')
    scaler = joblib.load('scaler.pkl')

    # Scale input data
    input_data_scaled = scaler.transform(input_data)

    # Make prediction
    predicted_price = lr_model.predict(input_data_scaled)

    return predicted_price[0]

def plot_rent_vs_size(file_path):
    # Load the data
    housing_data = pd.read_csv(file_path)
    
    # Create the figure
    fig, ax = plt.subplots()
    ax.scatter(housing_data['Size (sq ft)'], housing_data['Rent Price (ETB)'])
    ax.set_title('Rent Price vs Size of House')
    ax.set_xlabel('Size (sq ft)')
    ax.set_ylabel('Rent Price (ETB)')

    return fig  # Return the figure object

def plot_correlation_heatmap(file_path):
    # Load the CSV data
    housing_data = pd.read_csv(file_path)
    
    # One-hot encode categorical columns (like you did in the training phase)
    housing_data_encoded = pd.get_dummies(housing_data, columns=['Neighborhood', 'Condition'], drop_first=True)
    
    # Calculate the correlation matrix
    corr_matrix = housing_data_encoded.corr()

    # Create the heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    
    # Return the figure object for saving
    return plt.gcf()  # Return the current figure


def plot_rent_distribution(file_path):
    # Load the CSV data
    housing_data = pd.read_csv(file_path)

    # Create the distribution plot
    plt.figure(figsize=(10, 6))
    sns.histplot(housing_data['Rent Price (ETB)'], kde=True, color='purple', bins=20)
    plt.title('Distribution of Rent Prices')
    plt.xlabel('Rent Price (ETB)')
    plt.ylabel('Frequency')

    return plt.gcf()  # Return the current figure



def plot_interactive_rent_vs_size(file_path):
    # Load the CSV data
    housing_data = pd.read_csv(file_path)

    # Create an interactive scatter plot
    fig = px.scatter(housing_data, x='Size (sq ft)', y='Rent Price (ETB)', 
                     color='Neighborhood', 
                     size='Bedrooms',
                     hover_data=['Distance to City Center (km)', 'Condition'],
                     title='Rent Price vs. Size of House')
    
    # Generate the HTML for the Plotly figure
    plot_html = fig.to_html(full_html=False, include_plotlyjs='cdn')  # Use CDN to load Plotly.js

    return plot_html