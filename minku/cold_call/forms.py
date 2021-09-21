from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField()


class CommentForm(forms.Form):
    comment_content = forms.CharField(label="添加评论", widget=forms.Textarea(attrs={"rows":7, "cols":40}))
