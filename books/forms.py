from django import forms
from . import models


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ('text', )
        widgets = {
            'text': forms.Textarea(attrs={'class': 'book-comments-form__textarea', 'placeholder': 'Текст комментария'}),
        }
