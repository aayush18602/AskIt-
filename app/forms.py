from dataclasses import fields
from django import forms
from django.forms import ModelForm
from .models import Answer

class QuestionForm(forms.Form):
    qtitle = forms.CharField(max_length=300,label='Title')


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['ans']
