from django import forms
from django.core.exceptions import ValidationError
from .models import Complaint

MAX_FILE_SIZE_MB = 5

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['category', 'description', 'photo']

    def clean(self):
        cleaned_data = super().clean()
        photo = self.files.get('photo')

        if photo:
            if photo.size > MAX_FILE_SIZE_MB * 1024 * 1024:
                self.add_error('photo', f"File size exceeds {MAX_FILE_SIZE_MB}MB limit.")

            allowed_extensions = ('.jpg', '.jpeg', '.png', '.webp')
            if not photo.name.lower().endswith(allowed_extensions):
                self.add_error('photo', "Only JPG, PNG, and WebP images are allowed.")

        return cleaned_data