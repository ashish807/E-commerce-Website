from django import forms
from .models import ReviewRating, Appointments 

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']
        
class AppointmentForm(forms.ModelForm):
    class Meta:
        model =Appointments
        fields = ['first_name', 'last_name', 'phone', 'email', 'address_line_1', 'address_line_2', 'time', 'city', 'date']