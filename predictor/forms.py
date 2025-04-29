from django import forms
from .models import HousingData

class RentPredictionForm(forms.Form):
    size = forms.FloatField(label='Size (in square feet)', required=True)
    bedrooms = forms.IntegerField(label='Number of Bedrooms', required=True)
    bathrooms = forms.IntegerField(label='Number of Bathrooms', required=True)
    neighborhood = forms.ChoiceField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], label='Neighborhood', required=True)
    condition = forms.ChoiceField(choices=[('New', 'New'), ('Good', 'Good'), ('Average', 'Average')], label='Condition', required=True)
    distance = forms.FloatField(label='Distance to city center (in km)', required=True)

class UploadCSVForm(forms.ModelForm):
    class Meta:
        model = HousingData
        fields = ['csv_file']
        widgets = {
            'csv_file': forms.FileInput(attrs={'class': 'form-control'}),
        }
        
    def clean_csv_file(self):
        csv_file = self.cleaned_data.get('csv_file')

        # Ensure the file is not empty
        if not csv_file:
            raise forms.ValidationError("No file uploaded. Please select a CSV file.")

        # Check if the uploaded file is a CSV
        if not csv_file.name.endswith('.csv'):
            raise forms.ValidationError("Invalid file format. Please upload a CSV file.")
        
        return csv_file