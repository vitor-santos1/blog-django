from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Post

User = get_user_model()


class PostTests(TestCase):
    def setUp(self):
        self.autor = User.objects.create_user("autor", password="senha-forte-123")
        self.outro = User.objects.create_user("outro", password="senha-forte-123")
        self.post = Post.objects.create(title="Olá", content="Primeiro post", author=self.autor)

    def test_lista_publica(self):
        r = self.client.get(reverse("post_list"))
        self.assertContains(r, "Olá")

    def test_criar_exige_login(self):
        r = self.client.get(reverse("post_create"))
        self.assertEqual(r.status_code, 302)
        self.assertIn("/contas/login/", r.url)

    def test_criar_post(self):
        self.client.login(username="autor", password="senha-forte-123")
        r = self.client.post(reverse("post_create"), {"title": "Novo", "content": "Texto"})
        self.assertEqual(r.status_code, 302)
        self.assertTrue(Post.objects.filter(title="Novo", author=self.autor).exists())

    def test_editar_somente_autor(self):
        url = reverse("post_update", args=[self.post.pk])
        self.client.login(username="outro", password="senha-forte-123")
        self.assertEqual(self.client.post(url, {"title": "X", "content": "Y"}).status_code, 403)
        self.client.login(username="autor", password="senha-forte-123")
        self.client.post(url, {"title": "Editado", "content": "Y"})
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Editado")

    def test_excluir_somente_autor(self):
        url = reverse("post_delete", args=[self.post.pk])
        self.client.login(username="outro", password="senha-forte-123")
        self.assertEqual(self.client.post(url).status_code, 403)
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())
        self.client.login(username="autor", password="senha-forte-123")
        self.client.post(url)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_cadastro_de_usuario(self):
        r = self.client.post(
            reverse("signup"),
            {"username": "novo", "password1": "senha-forte-123", "password2": "senha-forte-123"},
        )
        self.assertEqual(r.status_code, 302)
        self.assertTrue(User.objects.filter(username="novo").exists())
