from django.test import TestCase, RequestFactory
from .models import Note, Tag, Comment
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from pathlib import Path

UserModel = get_user_model()


# Create your tests here.
class NotePostPageTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserModel.objects.create_user(
            email="user@test.edu",
            password="secret",
        )
        self.user_staff = UserModel.objects.create_customuser(
            email="staff@test.edu",
            password="secret",
            staff=True,
        )
        self.user_python = UserModel.objects.create_customuser(
            email="python@test.edu",
            password="secret",
            python_student=True,
        )
        tag_to_python = Tag.objects.create(
            tag_name="python_tag",
            search_word="python",
        )
        tag_to_subscribe = Tag.objects.create(
            tag_name="subscribe_tag",
            search_word="subscribe",
        )
        note_python = Note.objects.create(
            title="pyton_title",
            content="pyton_content",
            open_range="python_members",
            created_by=self.user,
        )

    # ログインしていない場合は404エラーを返す
    def test_should_return_404_if_user_does_not_login(self):
        url = reverse("note:note_post")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    # ログインしたときに200のステータスコードを返すか
    def test_should_return_200_if_user_login(self):
        self.client.force_login(self.user)
        url = reverse("note:note_post")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # データベースに作成した投稿が登録されているか
    def test_should_add_db_if_post(self):
        self.client.force_login(self.user_python)
        url = reverse("note:note_post")
        create_data = {"title": "title_test", "content": "content", "tags": "1", "open_range": "python_members"}
        response = self.client.post(url, create_data)
        q_counter = Note.objects.count()
        tag_to_note = Note.objects.filter(tags__pk=1).count()
        self.assertEqual(q_counter, 2)
        self.assertEqual(tag_to_note, 1)

    # 全てのタグが表示されるか
    def test_display_all_tags(self):
        self.client.force_login(self.user)
        url = reverse("note:note_post")
        response = self.client.get(url)
        self.assertContains(response, "python_tag")
        self.assertContains(response, "subscribe_tag")

    # python_student=falseの場合、open_range=python_membersへのリクエストは警告を表示する
    def test_alert_if_not_python_student(self):
        self.client.force_login(self.user)
        url = reverse("note:note_post")
        create_data = {"title": "title_test", "content": "content", "tags": "1", "open_range": "python_members"}
        response = self.client.post(url, create_data)
        self.assertContains(response, "許可されていない公開範囲です。")

    # 10MB以上のファイルは投稿に失敗する
    def test_limit_10MB_file_upload(self):
        self.client.force_login(self.user)
        url = reverse("note:note_post")
        file_10mb = Path(__file__).parent.parent / "test_file" / "testdata-10MB"
        with file_10mb.open(mode="rb") as f:
            create_data = {"title": "title_test", "content": "content", "tags": "1", "open_range": "python_members",
                           "attach_file": f}
            response = self.client.post(url, create_data)
        self.assertContains(response, "10MB以上のアップロードは禁止されています。")

    # postメソッドで302のリダイレクトのステータスコードを返し、投稿後のページが表示できるか
    def test_redirect_page_detail(self):
        self.client.force_login(self.user_python)
        url = reverse("note:note_post")
        create_data = {"title": "redirect_test", "content": "content", "tags": "1", "open_range": "python_members"}
        response = self.client.post(url, create_data)
        pk = Note.objects.get(title="redirect_test").pk
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("note:note_detail", kwargs={"pk": pk}))


class NoteListPageTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user_admin = UserModel.objects.create_superuser(
            email="admin@test.edu",
            password="secret",
        )
        self.user = UserModel.objects.create_user(
            email="user@test.edu",
            password="secret",
        )
        self.user_staff = UserModel.objects.create_customuser(
            email="staff@test.edu",
            password="secret",
            staff=True,
        )
        self.user_python = UserModel.objects.create_customuser(
            email="python@test.edu",
            password="secret",
            python_student=True,
        )
        note_public = Note.objects.create(
            title="public_title",
            content="public_content",
            open_range="public",
            created_by=self.user,
        )
        note_python = Note.objects.create(
            title="pyton_title",
            content="pyton_content",
            open_range="python_members",
            created_by=self.user,
        )
        note_subscribe = Note.objects.create(
            title="subscribe_title",
            content="subscribe_content",
            open_range="subscribers",
            created_by=self.user,
        )
        comment_to_note = Comment.objects.create(
            content="comment",
            created_by=self.user_python,
            note_to=note_python,
        )
        tag_to_python = Tag.objects.create(
            tag_name="python_tag",
            search_word="python",
        )
        tag_to_python.note_to.add(note_python)
        tag_to_subscribe = Tag.objects.create(
            tag_name="subscribe_tag",
            search_word="subscribe",
        )
        tag_to_subscribe.note_to.add(note_subscribe)

    # ログインしていないとき404エラーを返すか
    def test_should_return_404_if_user_does_not_login(self):
        url = reverse("note:note_list_range", kwargs={"range": "open"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    # ログインしたときに200のステータスコードを返すか
    def test_should_return_200_if_user_login(self):
        self.client.force_login(self.user)
        url = reverse("note:note_list_range", kwargs={"range": "public"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # indexへアクセスし、全ての記事が表示されるか
    def test_should_contain_all_if_access_to_index(self):
        self.client.force_login(self.user_admin)
        url = reverse("note:note_list_range", kwargs={"range": "index"})
        response = self.client.get(url)
        self.assertContains(response, "pyton_title")
        self.assertContains(response, "subscribe_title")
        self.assertContains(response, "public_title")

    # note/python_membersへアクセスし、pythonゼミのみ表示されるか
    def test_should_contain_python_if_python_student(self):
        self.client.force_login(self.user_python)
        url = reverse("note:note_list_group", kwargs={"group": "python_members"})
        response = self.client.get(url)
        self.assertContains(response, "pyton_title")
        self.assertNotContains(response, "subscribe_title")
        self.assertNotContains(response, "public_title")

    # note/subscribersへアクセスし、定額コース利用者のみ表示されるか
    def test_should_contain_subscribe_if_subscribers(self):
        self.client.force_login(self.user_staff)
        url = reverse("note:note_list_group", kwargs={"group": "subscribers"})
        response = self.client.get(url)
        self.assertNotContains(response, "pyton_title")
        self.assertContains(response, "subscribe_title")
        self.assertNotContains(response, "public_title")

    # note/publicへアクセスし、公開投稿のみ表示されるか
    def test_should_contain_public_if_public(self):
        self.client.force_login(self.user)
        url = reverse("note:note_list_range", kwargs={"range": "public"})
        response = self.client.get(url)
        self.assertNotContains(response, "pyton_title")
        self.assertNotContains(response, "subscribe_title")
        self.assertContains(response, "public_title")

    # user.staff = Trueの場合、定額コース利用とパブリックのみ表示されるか
    def test_should_contain_subscribe_if_user_is_staff(self):
        self.client.force_login(self.user_staff)
        url = reverse("note:note_list_range", kwargs={"range": "index"})
        response = self.client.get(url)
        self.assertNotContains(response, "pyton_title")
        self.assertContains(response, "subscribe_title")
        self.assertContains(response, "public_title")

    # user.python_student = Trueの場合、Pythonゼミとパブリックのみ表示されるか
    def test_should_contain_python_if_user_is_python(self):
        self.client.force_login(self.user_python)
        url = reverse("note:note_list_range", kwargs={"range": "index"})
        response = self.client.get(url)
        self.assertContains(response, "pyton_title")
        self.assertNotContains(response, "subscribe_title")
        self.assertContains(response, "public_title")

    # userが権限がない場合、パブリックのみ表示されるか
    def test_should_contain_public_if_user_is_user(self):
        self.client.force_login(self.user)
        url = reverse("note:note_list_range", kwargs={"range": "index"})
        response = self.client.get(url)
        self.assertNotContains(response, "pyton_title")
        self.assertNotContains(response, "subscribe_title")
        self.assertContains(response, "public_title")

    # user.python_student=Tureでindexへアクセスし、pythonゼミの記事のタグのみ表示されるか
    def test_should_display_only_python_tag(self):
        self.client.force_login(self.user_python)
        url = reverse("note:note_list_range", kwargs={"range": "index"})
        response = self.client.get(url)
        self.assertContains(response, "python_tag")
        self.assertNotContains(response, "subscribe_tag")

    # user.staff=Tureでindexへアクセスし、定額コースの記事のタグのみ表示されるか
    def test_should_display_only_subscribe_tag(self):
        self.client.force_login(self.user_staff)
        url = reverse("note:note_list_range", kwargs={"range": "index"})
        response = self.client.get(url)
        self.assertNotContains(response, "python_tag")
        self.assertContains(response, "subscribe_tag")

    # user.python_student=Trueの場合,Pythonゼミ参加者の絞り込みが表示されるか
    def test_should_display_python_search_if_user_python(self):
        self.client.force_login(self.user_python)
        url = reverse("note:note_list_range", kwargs={"range": "index"})
        response = self.client.get(url)
        self.assertContains(response, "Pythonゼミ参加者")
        self.assertNotContains(response, "定額コース利用者限定")

    # user.staff=Trueの場合,定額コース利用者限定の絞り込みが表示されるか
    def test_should_display_subscribers_search_if_user_staff(self):
        self.client.force_login(self.user_staff)
        url = reverse("note:note_list_range", kwargs={"range": "index"})
        response = self.client.get(url)
        self.assertNotContains(response, "Pythonゼミ参加者")
        self.assertContains(response, "定額コース利用者限定")

    # tag/pythonで、対象の記事のみ表示されるか
    def test_should_display_note_match_tag(self):
        self.client.force_login(self.user_admin)
        url = reverse("note:note_list_tag", kwargs={"tag_word": "python"})
        response = self.client.get(url)
        self.assertContains(response, "pyton_title")
        self.assertNotContains(response, "subscribe_title")
        self.assertNotContains(response, "public_title")

    # tag/pythonで、対象のタグのみ表示されるか
    def test_should_display_match_tag(self):
        self.client.force_login(self.user_admin)
        url = reverse("note:note_list_tag", kwargs={"tag_word": "python"})
        response = self.client.get(url)
        self.assertContains(response, "python_tag")
        self.assertNotContains(response, "subscribe_tag")

    # 絞り込みにpostし、対象の記事のみ表示されるか

    # コメントの件数が表示されるか
    def test_should_display_comment_number(self):
        self.client.force_login(self.user_python)
        url = reverse("note:note_list_group", kwargs={"group": "python_members"})
        response = self.client.get(url)
        self.assertContains(response, "コメント数：1件")
        self.assertNotContains(response, "コメント数：0件")


class NoteDetailPageTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserModel.objects.create_user(
            email="user@test.edu",
            password="secret",
        )
        self.user_python = UserModel.objects.create_customuser(
            email="python@test.edu",
            password="secret",
            python_student=True,
        )
        note_public = Note.objects.create(
            title="public_title",
            content="public_content",
            open_range="public",
            created_by=self.user_python,
        )
        note_pyton = Note.objects.create(
            title="python_title",
            content="python_content",
            open_range="python_members",
            created_by=self.user_python,
        )

    def test_should_return_404_if_user_does_not_login(self):
        url = reverse("note:note_detail", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    # ログインしたときに200のステータスコードを返すか
    def test_should_return_200_if_user_login(self):
        self.client.force_login(self.user_python)
        url = reverse("note:note_detail", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # python_studentの権限を持っていない場合、404エラーを返すか
    def test_return_404_if_not_python_student(self):
        self.client.force_login(self.user)
        url = reverse("note:note_detail", kwargs={"pk": 2})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    # 添付ファイルがある場合、attached fileが表示されるか

    # commentをpostし、データベースに登録されるか
    def test_add_db_if_post(self):
        self.client.force_login(self.user)
        url = reverse("note:note_detail", kwargs={"pk": 1})
        create_data = {"content": "comment_1"}
        response = self.client.post(url, create_data)
        q_counter = Comment.objects.filter(content="comment_1").count()
        self.assertEqual(q_counter, 1)

    # postした後、302のステータスコードを返すか
    def test_redirect_page_detail(self):
        self.client.force_login(self.user)
        url = reverse("note:note_detail", kwargs={"pk": 1})
        create_data = {"content": "comment_2"}
        response = self.client.post(url, create_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("note:note_detail", kwargs={"pk": 1}))

    # postした後、作成したcommentがページに表示されるか
    def test_contain_comment_if_post(self):
        self.client.force_login(self.user)
        url = reverse("note:note_detail", kwargs={"pk": 1})
        create_data = {"content": "comment_3"}
        response = self.client.post(url, create_data)
        get_response = self.client.get(url)
        self.assertContains(get_response, "comment_3")

    # 紐づけられたタグを表示しているか

    # 投稿範囲が表示されているか
