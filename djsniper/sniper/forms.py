from django import forms
from .models import NFTProject, Category


class ProjectForm(forms.ModelForm):
    class Meta:
        model = NFTProject
        fields = '__all__'

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class ConfirmForm(forms.Form):
    hidden = forms.HiddenInput()
