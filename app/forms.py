from dataclasses import fields
from django import forms
from django.forms import ModelForm
from .models import Answer,Comment
from mptt.forms import TreeNodeChoiceField

class QuestionForm(forms.Form):
    qtitle = forms.CharField(max_length=300,label='Title')


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['ans']

class CommentForm(ModelForm):
    parent = TreeNodeChoiceField(queryset=Comment.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['parent'].label = ''
        self.fields['content'].label = 'Comment'
        self.fields['parent'].widget.attrs.update( 
            {'class': 'd-none'}
        )
        self.fields['parent'].required = False

    class Meta:
        model = Comment
        fields = ['parent','content']
        widgets = {
            'content':forms.TextInput(attrs={'style':'border-radius:10px;border:2px solid black;'})
        }
            
