import os
import pandas as pd
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import RentPredictionForm, UploadCSVForm
from .models import HousingData
from .ml_model import predict_rent, train_model, plot_rent_vs_size, plot_rent_distribution, plot_correlation_heatmap, plot_interactive_rent_vs_size

from django.contrib import messages  # For success/error messages
import os
import traceback
 

def upload_csv(request):
    error_message = None
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            # Delete old CSV files and upload new one
            HousingData.objects.all().delete()
            instance = form.save()
            csv_file_path = os.path.join(settings.MEDIA_ROOT, str(instance.csv_file))

            try:
                if not csv_file_path.endswith('.csv'):
                    error_message = "Invalid file format. Please upload a CSV file."
                    messages.error(request, error_message)
                    return redirect('upload_csv')

                # Train model with uploaded CSV
                success_message = train_model(csv_file_path)
                messages.success(request, success_message)

                # Define the plot directory
                plot_directory = os.path.join(settings.MEDIA_ROOT, 'plots')
                os.makedirs(plot_directory, exist_ok=True)  # Ensure the directory exists

                # Generate and save plot files in 'media/plots' directory
                plot_rent_vs_size(csv_file_path).savefig(os.path.join(plot_directory, 'rent_vs_size.png'))
                plot_correlation_heatmap(csv_file_path).savefig(os.path.join(plot_directory, 'correlation_heatmap.png'))
                plot_rent_distribution(csv_file_path).savefig(os.path.join(plot_directory, 'rent_distribution.png'))

                # Generate the interactive plot as HTML
                plot_html = plot_interactive_rent_vs_size(csv_file_path)
                with open(os.path.join(plot_directory, 'interactive_rent_vs_size.html'), 'w') as f:
                    f.write(plot_html)

                return redirect('home')  # Redirect to the home page

            except Exception as e:
                print("An error occurred while training the model:")
                traceback.print_exc()  # Print the full stack trace for debugging
                error_message = f"An error occurred: {str(e)}"
                messages.error(request, error_message)
        else:
            error_message = form.errors.get('csv_file')
            messages.error(request, error_message)

    else:
        form = UploadCSVForm()

    return render(request, 'predictor/upload_csv.html', {'form': form, 'error_message': error_message})

def home(request):
    predicted_price = None
 
    if not HousingData.objects.exists():
        return render(request, 'predictor/no_csv.html') 
    
    form = RentPredictionForm()

    if request.method == 'POST':
        form = RentPredictionForm(request.POST)
        if form.is_valid():
            # Extract form data
            size = form.cleaned_data['size']
            bedrooms = form.cleaned_data['bedrooms']
            bathrooms = form.cleaned_data['bathrooms']
            neighborhood = form.cleaned_data['neighborhood']
            condition = form.cleaned_data['condition']
            distance = form.cleaned_data['distance']

            # Prepare data for prediction
            input_data = pd.DataFrame({
                'Size (sq ft)': [size],
                'Bedrooms': [bedrooms],
                'Bathrooms': [bathrooms],
                'Distance to City Center (km)': [distance],
                'Neighborhood_B': [1 if neighborhood == 'B' else 0],
                'Neighborhood_C': [1 if neighborhood == 'C' else 0],
                'Neighborhood_D': [1 if neighborhood == 'D' else 0],
                'Condition_Good': [1 if condition == 'Good' else 0],
                'Condition_New': [1 if condition == 'New' else 0]
            })

            # Make prediction
            predicted_price = predict_rent(input_data)

            # Get the latest uploaded CSV file path
            
        
            
    return render(request, 'predictor/home.html', {
        'form': form,
        'predicted_price': predicted_price,
    })
    

def graph_view(request):
    # Define paths to each plot in the 'media/plots' directory
    plot_urls = {
        'rent_vs_size': os.path.join(settings.MEDIA_URL, 'plots/rent_vs_size.png'),
        'correlation_heatmap': os.path.join(settings.MEDIA_URL, 'plots/correlation_heatmap.png'),
        'rent_distribution': os.path.join(settings.MEDIA_URL, 'plots/rent_distribution.png'),
    }
    
    # Path to the interactive plot HTML file
    interactive_plot_path = os.path.join(settings.MEDIA_ROOT, 'plots', 'interactive_rent_vs_size.html')

    # Read the HTML content of the interactive plot
    plot_html = ''
    if os.path.exists(interactive_plot_path):
        with open(interactive_plot_path, 'r') as f:
            plot_html = f.read()  # Read the HTML content of the file

    return render(request, 'predictor/graph.html', {
        'plot_urls': plot_urls,
        "plot_html": plot_html  # Pass the HTML content
    })