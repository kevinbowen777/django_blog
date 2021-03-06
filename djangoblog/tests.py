from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse

from .models import Post
from .views import AboutPageView


class BlogTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="johndoe",
            email="johndoe.example.com",
            password="secret",
        )

        self.post = Post.objects.create(
            title="A good title",
            body="Nice body content",
            author=self.user,
        )

    def test_post___str__(self):
        self.assertEqual(str(self.post), self.post.title)

    def test_post_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), "/post/1/")

    def test_post_content(self):
        self.assertEqual(f"{self.post.title}", "A good title")
        self.assertEqual(f"{self.post.author}", "johndoe")
        self.assertEqual(f"{self.post.body}", "Nice body content")

    def test_post_list_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nice body content")
        self.assertTemplateUsed(response, "home.html")

    def test_post_detail_view(self):
        response = self.client.get("/post/1/")
        no_response = self.client.get("post/100000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "A good title")
        self.assertTemplateUsed(response, "posts/post_detail.html")

    """
    Note: need to understand objects.last better
    def test_post_create_view(self):
        response = self.client.post(
            reverse("post_new"),
            {
                "title": "New title",
                "body": "New text",
                "author": self.user.id,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, "A good title")
        self.assertEqual(Post.objects.last().body, "Nice body content")
        # self.assertEqual(Post.objects.title, "New title")
        # self.assertEqual(Post.objects.body, "New text")
    """

    def test_post_update_view(self):
        response = self.client.post(
            reverse("post_edit", args="1"),
            {
                "title": "Updated title",
                "body": "Updated text",
            },
        )
        self.assertEqual(response.status_code, 302)

    def test_post_delete_view(self):
        response = self.client.post(reverse("post_delete", args="1"))
        self.assertEqual(response.status_code, 302)


class AboutPageTests(TestCase):
    def setUp(self):
        url = reverse("about")
        self.response = self.client.get(url)

    def test_aboutpage_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_aboutpage_template(self):
        self.assertTemplateUsed(self.response, "about.html")

    def test_aboutpage_contains_correct_html(self):
        self.assertContains(self.response, "About Page")

    def test_aboutpage_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "This doesn't belong here")

    def test_aboutpage_url_resolves_aboutpageview(self):
        view = resolve("/about/")
        self.assertEqual(view.func.__name__, AboutPageView.as_view().__name__)
