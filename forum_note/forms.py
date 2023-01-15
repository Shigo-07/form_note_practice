from django import forms
from django.core.exceptions import ValidationError
import forum_note.models
from .models import Tag, Comment


class NewNoteForm(forms.Form):
    choices = (('public', "公開"), ("login", "ログインユーザー限定"), ('subscribers', '定額コース利用者限定'),
               ('python_members', 'Pythonゼミ参加者'))
    title = forms.CharField(label="タイトル", max_length=128)
    tags = forms.ModelMultipleChoiceField(required=False, queryset=Tag.objects,
                                          widget=forms.CheckboxSelectMultiple)
    content = forms.CharField(label="本文", widget=forms.Textarea)
    attach_file = forms.FileField(label="添付", required=False)
    attach_image = forms.ImageField(label="画像", required=False)
    is_publish_mail = forms.BooleanField(label="グループ向けの朝のサマリーメールに含める", widget=forms.CheckboxInput, required=False)
    open_range = forms.ChoiceField(label="公開範囲", choices=choices, widget=forms.RadioSelect)

    def clean_open_range(self):
        open_range = self.cleaned_data["open_range"]
        user = self.user
        if open_range == "python_members":
            if not user.python_student:
                raise forms.ValidationError("投稿が許可されていない公開範囲です。")
        elif open_range == "subscribers":
            if not user.staff:
                raise forms.ValidationError("投稿が許可されていない公開範囲です。")
        return open_range

    def validate_file_size(self, file):
        if hasattr(file, "size"):
            FILE_SIZE = 1 * 1000 * 1000
            if file.size > FILE_SIZE:
                raise ValidationError(
                    f'10MB以上のアップロードは禁止されています。※アップロードされたファイルサイズ：{file.size // 1000 // 1000}MB'
                )

    def clean_attach_file(self):
        attach_file = self.cleaned_data["attach_file"]
        self.validate_file_size(file=attach_file)
        return attach_file

    def clean_attach_image(self):
        attach_image = self.cleaned_data["attach_image"]
        self.validate_file_size(file=attach_image)
        return attach_image


class CommentForm(forms.ModelForm):
    attach_file = forms.FileField(label="添付", required=False)
    attach_image = forms.ImageField(label="画像", required=False)

    def validate_file_size(self, file):

        if hasattr(file, "size"):
            FILE_SIZE = 1 * 1000 * 1000
            if file.size > FILE_SIZE:
                print("over_file_size")
                raise ValidationError(
                    f'10MB以上のアップロードは禁止されています。※アップロードされたファイルサイズ：{file.size // 1000 // 1000}MB'
                )

    def clean_attach_file(self):

        attach_file = self.cleaned_data["attach_file"]
        self.validate_file_size(file=attach_file)
        return attach_file

    def clean_attach_image(self):

        attach_image = self.cleaned_data["attach_image"]
        self.validate_file_size(file=attach_image)
        return attach_image

    class Meta:
        model = Comment
        fields = ('content', 'attach_file', 'attach_image', 'is_publish_mail')
        labels = {
            "content": "コメント:",
            "attach_file":"添付:",
            "attach_image": "画像:",
            "is_publish_mail": "グループ向けの朝のサマリーメールに含める"
        }
