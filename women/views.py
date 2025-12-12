from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from .utils import DateMixin
import time

from django.template.loader import render_to_string

from .models import Women, Category, TagPost, UploadFile
from .forms import AddPostForm, UploadFileForm


class WomenHome(DateMixin, ListView):
    template_name = "women/index.html"
    context_object_name = "posts"
    title_page = "Главная страница"
    cat_selected = 0

    def get_queryset(self):
        return Women.published.all().select_related("cat")


class WomenCategory(DateMixin, ListView):
    template_name = "women/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs["cat_slug"]).select_related("cat")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context["posts"][0].cat
        return super().get_mixin_context(context, title=cat.name, cat_selected=cat.pk)


class ShowPost(DateMixin, DetailView):
    model = Women
    template_name = "women/post.html"
    context_object_name = "post"
    slug_url_kwarg = "post_slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return super().get_mixin_context(context, title=context["post"].title, cat_selected=context["post"].cat.id)

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])


class TagPostList(DateMixin, ListView):
    template_name = "women/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(tag__slug=self.kwargs["tag_slug"]).select_related("cat")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs["tag_slug"])
        return super().get_mixin_context(context, title="Тег: " + tag.name, tag_selected=tag.id)


class AddPage(LoginRequiredMixin, DateMixin, CreateView):
    form_class = AddPostForm
    template_name = "women/add_page.html"
    success_url = reverse_lazy("home")
    title_page = "Добавление статьи"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdatePage(DateMixin, UpdateView):
    model = Women
    fields = ["title", "content", "photo", "is_published", "cat", "husband", "tag"]
    template_name = "women/add_page.html"
    success_url = reverse_lazy("home")
    title_page = "Добавление статьи"


class DeletePage(DateMixin, DeleteView):
    model = Women
    template_name = "women/delete_page.html"
    success_url = reverse_lazy("home")
    title_page = "Удаление статьи"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return super().get_mixin_context(context, name=context["object"].title)


class About(DateMixin, View):
    template_name = "women/about.html"
    title_page = "О сайте"
    context = {}

    def get(self, request):
        form = UploadFileForm()
        return render(request, self.template_name,
                      context=super().get_mixin_context(self.context, form=form))

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFile(file=form.cleaned_data["file"])
            fp.save()
        return render(request, self.template_name,
                      context=super().get_mixin_context(self.context, form=form))


@login_required()
def about(request):
    list_page = Women.published.all()
    paginator = Paginator(list_page, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, template_name="women/about.html",
                  context={
                      "title": "О сайте",
                      "page_obj": page_obj
                  })


def handler_upload_files(f):
    with open(f"uploads/{time.strftime('%H:%M:%S')}-{f.name}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
