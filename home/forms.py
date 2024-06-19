from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime

class TimetableForm(forms.Form):
    time_slot = forms.TimeField(
        widget=forms.TimeInput(format='%H:%M'),
        input_formats=['%H:%M'],
        required=True
    )
    date = forms.DateField(
        widget=forms.DateInput(format='%Y-%m-%d'),
        input_formats=['%Y-%m-%d'],
        required=True
    )
    task_activity = forms.CharField(max_length=255, required=True)
    description = forms.CharField(widget=forms.Textarea, required=False)
    status = forms.ChoiceField(
        choices=[
            ('Planned', 'Planned'),
            ('In Progress', 'In Progress'),
            ('Completed', 'Completed'),
        ],
        required=True
    )
    recurring = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(TimetableForm, self).__init__(*args, **kwargs)
        # Set the input type for the 'date' field to 'date'
        self.fields['date'].widget.input_type = 'date'
        # Set the input type for the 'time_slot' field to 'time'
        self.fields['time_slot'].widget.input_type = 'time'

    def clean(self):
        cleaned_data = super().clean()
        current_time = datetime.now().time()
        current_date = datetime.now().date()

        # Validate that the time_slot is not before the current time

        # Validate that the date is not before the current date
        if 'date' in cleaned_data and cleaned_data['date'] < current_date:
            raise ValidationError("Date cannot be before the current date.")
        elif 'date' in cleaned_data and cleaned_data['date'] == current_date and 'time_slot' in cleaned_data and cleaned_data['time_slot'] < current_time:
            raise ValidationError("Time cannot be before the current time.")

        return cleaned_data
    
    
    
    
    
    
from django import forms
from notes.models import Article
from django_ckeditor_5.widgets import CKEditor5Widget
from django.contrib.auth.models import User  

class NoteForm(forms.ModelForm):
    text = CKEditor5Widget(config_name='extends') 
    class Meta:
        model = Article
        fields = ['title', 'text'] 



