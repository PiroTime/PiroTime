from django import forms
from .models import CoffeeChat

class CoffeeChatForm(forms.ModelForm):
    hashtags = forms.CharField(widget=forms.HiddenInput(), required=False)
    content = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = CoffeeChat
        fields = ['job', 'hashtags', 'content']

