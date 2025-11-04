from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comment', 'image']
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': 3, 
                'placeholder': 'Write your feedback here...'
            }),
        }