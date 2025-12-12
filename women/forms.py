from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible
from .models import Category, Husband, Women


@deconstructible
class RussianValidator:
    ALLOWED_CHARS = "ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЁЯЧСМИТЬБЮйцукенгшщзхъфывапролджэёячсмитьбю- "
    code = "russian"

    def __init__(self, message=None):
        self.message = message if message else "Только русские символы, дефис и пробел"

    def __call__(self, value, *args, **kwargs):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, self.code)


class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Не выбрано", label="Категории")
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), empty_label="Не замужем", label="Мужья",
                                     required=False)

    class Meta:
        model = Women
        fields = ["title", "content", "photo", "is_published", "cat", "husband"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-input"}),
            "content": forms.Textarea(attrs={"cols": 50, "rows": 5})
        }
        labels = {
            "slug": "URL"
        }

    def clean_title(self):
        title = self.cleaned_data["title"]
        if len(title) > 50:
            raise ValidationError("Заголовок должен быть меньше 50 символов")
        return title


class UploadFileForm(forms.Form):
    file = forms.ImageField(label="Файл")
