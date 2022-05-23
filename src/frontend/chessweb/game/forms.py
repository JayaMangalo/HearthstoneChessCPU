from django import forms

class ActionForm(forms.Form):
    ACTION = forms.CharField(label='ACTION', max_length=100)