from django.db import models

class HousingData(models.Model):
    csv_file = models.FileField(upload_to='csv_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"CSV uploaded at {self.uploaded_at}"
