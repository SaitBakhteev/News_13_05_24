import datetime

from django import forms
from .models import Post, Author, Category
from django.core.exceptions import ValidationError
from datetime import datetime

class PostForm(forms.Form):
    author = forms.ModelChoiceField(label='Автор', queryset=Author.objects.all(), required=False)
    postType=forms.ChoiceField(label='Тип публикации',choices=Post.post_type)
    create_time = forms.DateTimeField (disabled=True, label='Дата создания публикации')
    # category=forms.SelectMultiple(choices=Category.objects.all())
    title = forms.CharField(label='Заголовок публикации', max_length=50)
    content= forms.CharField(label='Содержание публикации', widget=forms.Textarea)


    def clean(self): # проверка не слишком ли короткое название
        check=super().clean()
        title=check.get('title')
        if len(title)<5:
            raise ValidationError({'title':'Слишком короткое название.'})
        return check

    def get_context(self):
        context=super().get_context()
        return context

    # def definition_fields(self, post:Post):

