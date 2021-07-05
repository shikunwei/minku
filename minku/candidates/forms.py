from django import forms


PLATFORM_CHOICES = (('猎聘', '猎聘'),)


class ReadCandidateInfoForm(forms.Form):
    candidate_url = forms.CharField(label="URL", widget=forms.TextInput)
    # candidate_platform = forms.CharField(label="平台", widget=forms.RadioSelect(choices=PLATFORM_CHOICES))
    # price = forms.CharField(label="用户名: ", widget=forms.TextInput)
    # bedroom = forms.CharField(label="密码: ", widget=forms.TextInput)


class UploadFileForm(forms.Form):
    file = forms.FileField()


class CommentForm(forms.Form):
    comment_content = forms.CharField(label="添加备注", widget=forms.Textarea(attrs={"rows":7, "cols":40}))
