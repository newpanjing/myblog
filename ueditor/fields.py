from __future__ import absolute_import

from django import forms
from django.db import models

from .widgets import UEditorWidget


class RichTextField(models.TextField):

    def __init__(self, *args, **kwargs):
        self.config = kwargs.pop("config", {})
        # self.extra_plugins = kwargs.pop("extra_plugins", [])
        # self.external_plugin_resources = kwargs.pop("external_plugin_resources", [])
        super(RichTextField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': self._get_form_class(),
            'config': self.config,
        }
        defaults.update(kwargs)
        return super(RichTextField, self).formfield(**defaults)

    @staticmethod
    def _get_form_class():
        return RichTextFormField


class RichTextFormField(forms.fields.CharField):

    def __init__(self, config={}, *args, **kwargs):
        kwargs.update({'widget': UEditorWidget(config=config)})
        super(RichTextFormField, self).__init__(*args, **kwargs)
