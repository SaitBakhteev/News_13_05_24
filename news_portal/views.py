# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, UpdateView, View
from django.shortcuts import render
from .models import Post, Comment
from .filters import PostFilter
from .forms import PostForm
from pprint import pprint

class PostsList(ListView): #класс для показа общего списка всепх публикаций
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    # ordering = 'create_time'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'flatpages/news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'post'
    # queryset = Post.objects.all().order_by('title')
    paginate_by = 10

    def context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        return context

class PostDetail(DetailView): # детальная информация конкретного поста
    model = Post
    template_name = 'flatpages/update_post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs): # модернизация контекста для отображения комментариев
                                                # на отдельной странице поста
        context=super().get_context_data(**kwargs)
        context['comm'] = Comment.objects.filter(post_id=self.kwargs['pk'])

        form=PostForm(initial={'title': self.object.title,
                        'content': self.object.content,
                       'create_time': self.object.create_time,
                        'author': self.object.author})

        context['form'] = form
        form.fields['content'].disabled = True
        pprint(context)

        return context

class PostFilterView(ListView): # класс для отображения фильтра поста на отдельной HTML странице 'search.html'
    model = Post
    template_name = 'flatpages/search.html'
    context_object_name = 'post'
    paginate_by =3

    def get_queryset(self):
        queryset=super().get_queryset()
        self.filter = PostFilter(self.request.GET,queryset)
        return self.filter.qs

    def get_context_data(self,  **kwargs): #добавление в контекст фильтра
        context=super().get_context_data(**kwargs)
        context['filter']=self.filter
        # pprint(context)
        return context

def create_post(request): # функция для создания и добавления новой публикации
    form=PostForm()
    if request.method=='POST':
        form=PostForm(request.POST)
        if form.is_valid():
            Post.objects.create(**form.cleaned_data)
            return HttpResponseRedirect('/news/')
    return render(request, 'flatpages/create_post.html', {'form':form})

def update_post(request, pk): # функция для редактирования статей
    post = Post.objects.get(pk=pk)
    state = '' # переменная, сигнализирующая об удачном редактировании статьи
    form=PostForm(initial={'title':post.title,
                           'content':post.content,
                           'create_time':post.create_time,
                           'category':post.category,
                           'author':post.author
                           })
    form.fields['author'].disabled = True

    if request.method=='POST':
        form=PostForm(request.POST,post)
        if form.is_valid():
            Post.objects.filter(pk=pk).update(**{'title':form.cleaned_data['title'],
                                                 'content':form.cleaned_data['content'],
                                                 'author':form.cleaned_data['author_show'],}
                                              )
            state = 'Изменения в статье успешно сохранены.'

    return render(request, 'flatpages/update_post.html', {'form':form, 'post':post, 'state':state})


# Неиспользуемые классы ниже
class CommListView(ListView):  # класс для отобрпажения
    model = Comment
    template_name = 'flatpages/comm.html'
    context_object_name = 'cmts'