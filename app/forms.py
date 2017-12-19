from django import forms
from app.models import Info


class UploadFileForm(forms.Form):
	file = forms.FileField()
	def clean(self):
		files = self.cleaned_data.get("file")
		if files:
			filename = files.name
			if filename.endswith('.xls') or filename.endswith('.xlsx') or filename.endswith('.csv'):
				return files
			else:
				raise forms.ValidationError("Unsupported File type.")
		return files
		class meta:
			('file',)


class AddInfoForm(forms.ModelForm):
	class Meta:
		model = Info
		fields = ('ttype','name','amount','date')