# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.shortcuts import render
from .models import Post, Comment
from .filters import PostFilter
from .forms import PostForm

class PostsList(ListView):
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
    template_name = 'flatpages/post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs): # модернизация контекста для отображения комментариев
                                                # на отдельной странице поста
        context=super().get_context_data(**kwargs)
        context['comm'] = Comment.objects.filter(post_id=self.kwargs['pk'])
        return context

def create_post(request):
    form=PostForm()
    if request.method=='POST':
        form=PostForm(request.POST)
        if form.is_valid():
            new_post=Post(content=form.cleaned_data['content_x'], title=form.cleaned_data['title_x'], author=form.cleaned_data['author_x'] )
            new_post.save()
            return HttpResponseRedirect('/news/')
    return render(request, 'flatpages/create_post.html', {'form':form})


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

class CommListView(ListView):
    model = Comment
    template_name = 'flatpages/comm.html'
    context_object_name = 'cmts'


