from django import forms
from .models import Resume, JobRole, Question
from dal import autocomplete
from .models import Answer


class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['file']


class JobPreferenceForm(forms.Form):
    job_role = forms.ModelChoiceField(
        queryset=JobRole.objects.filter(is_active=True),
        widget=autocomplete.ModelSelect2(url='job-role-autocomplete')
    )


# New FilterForm for questions
class FilterForm(forms.Form):
    DIFFICULTY_CHOICES = [
        ('', 'All'),
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard')
    ]

    difficulty = forms.ChoiceField(
        choices=DIFFICULTY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    job_role = forms.ModelChoiceField(
        queryset=JobRole.objects.filter(is_active=True),
        required=False,
        empty_label="All Job Roles",
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer_text', 'answer_audio']
        widgets = {
            'answer_text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Type your answer here...'}),
        }
