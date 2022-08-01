from django import forms
from django.db import models


class SelectLanguageFormClass(forms.Form):
    TECHNIQUE = (('rails', 'Ruby on Rails'), ('django', 'Django'))
    # technique = forms.ChoiceField(label="言語及びフレームワーク", choices=TECHNIQUE)
    technique = forms.CharField(label="言語及びフレームワーク", initial='rails')

class SelectErrorsFormClass(forms.Form):
    TECHNIQUE = (('rails', 'Ruby on Rails'), ('django', 'Django'))
    # ERROR_MESSAGE = (('',''),('',''),('',''),('',''))
    #technique = forms.ChoiceField(label="言語及びフレームワーク", choices=TECHNIQUE)
    technique = forms.CharField(label="言語及びフレームワーク", initial='rails')
    # error_message = forms.ChoiceField(label="エラーメッセージ", choices=ERROR_MESSAGE)
    error_message = forms.CharField(widget=forms.Textarea)
    Feature = forms.CharField()

    def __init__(self, *args, **kwargs):
        for field in self.base_fields.values():
            field.widget.attrs["class"] = "form-control"
        super().__init__(*args, **kwargs)
