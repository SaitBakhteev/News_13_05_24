from django import forms
from .models import Post, Author
from django.core.exceptions import ValidationError


class PostForm(forms.Form):
    title_x = forms.CharField(label='Заголовок публикации', max_length=50)
    content_x= forms.CharField(label='Содержание публикации', widget=forms.Textarea)
    author_x=forms.ModelChoiceField(label='Автор', queryset=Author.objects.all())


    class Meta:
        model = Post
        fields=['author','title','content','postType']

    def clean(self):
        clean_post = super().clean()
        title = clean_post.get('title')
        if len(title)<5:
            raise ValidationError({'title':'Нельзя писать плохиев слова'})
        return clean_post
