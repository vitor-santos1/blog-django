from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import PostForm, SignUpForm
from .models import Post


class PostListView(ListView):
    model = Post
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.select_related("author")


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Publicação criada com sucesso.")
        return super().form_valid(form)


class AuthorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Somente o autor da publicação pode editar ou excluir."""

    def test_func(self):
        return self.get_object().author == self.request.user


class PostUpdateView(AuthorRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        messages.success(self.request, "Publicação atualizada.")
        return super().form_valid(form)


class PostDeleteView(AuthorRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("post_list")

    def form_valid(self, form):
        messages.success(self.request, "Publicação excluída.")
        return super().form_valid(form)


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("post_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response
