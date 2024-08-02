from django import forms

from corboard.models import Corboard, Comment


class CorboardForm(forms.ModelForm):
    class Meta:
        model = Corboard
        fields = ['title', 'content', 'corboardImg']

class CorCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']