from django.test import TestCase
from .models import Note,Tag,Comment
from django.contrib.auth import get_user_model

UserModel = get_user_model()
# Create your tests here.
class NoteListPageTest(TestCase):
    pass
    # URLとビュー関数が一致しているか

    # ログインしていないとき404エラーを返すか

    # ログインしたときに200のステータスコードを返すか

    # python_studentの権限を持っているとき、Pythonゼミ参加者が表示されているか

    # indexへアクセスし、全ての記事が表示されるか

    # python_membersへアクセスし、pythonゼミのみ表示されるか

    # subscribersへアクセスし、定額コース利用者のみ表示されるか

    # タグを選択肢し、対象の記事のみ表示されるか

    # 絞り込みにpostし、対象の記事のみ表示されるか


class NotePostPageTest(TestCase):
    pass
    # ログインしていないとき404エラーを返すか

    # URLとビュー関数が一致しているか

    # ログインしたとき200のステータスコードを返すか

    # postメソッドで302のリダイレクトのステータスコードを返すか

    # 投稿後のページを表示しているか

    # データベースに作成した投稿が登録されているか

    # 空の送信時に400エラーを返すか

    # python_studentの権限を持っている場合、投稿範囲にpythonゼミ限定を表示するか

    # python_studentの権限を持っている場合、投稿範囲にpythonゼミ限定を表示されないか

class NoteDetailPageTest(TestCase):
    pass
    # ログインしていないとき404エラーを返すか

    # python_studentの権限を持っていない場合、404エラーを返すか

    # URLとビュー関数が一致しているか

    # ログインしたとき200のステータスコードを返すか

    # 添付ファイルがある場合、attached fileが表示されるか

    # commentをpostし、データベースに登録されるか

    # postした後、201のステータスコードを返すか

    # postした後、作成したcommentがページに表示されるか