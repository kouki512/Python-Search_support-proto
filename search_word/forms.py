from django import forms
from django.db import models


class SelectLanguageFormClass(forms.Form):
    TECHNIQUE = (('rails', 'Ruby on Rails'), ('django', 'Django'))
    technique = forms.ChoiceField(label="言語及びフレームワーク", choices=TECHNIQUE)


class SelectErrorsFormClass(forms.Form):
    TECHNIQUE = (('rails', 'Ruby on Rails'), ('django', 'Django'))
    ERROR_MESSAGE = (('',''),('',''))
    technique = forms.ChoiceField(label="言語及びフレームワーク", choices=TECHNIQUE)
    error_message = forms.ChoiceField(label="エラーメッセージ", choices=TECHNIQUE)
    error_details = forms.CharField()

    def __init__(self, *args, **kwargs):
        for field in self.base_fields.values():
            field.widget.attrs["class"] = "form-control"
        super().__init__(*args, **kwargs)
