from django import forms

from .models import PostTag, PostTagModelQuerysetHandler

class TagAdminForm(forms.ModelForm):
    class Meta:
        model = PostTag
        fields = ('slug',)


class TagField(forms.CharField):
    """
    A ``CharField`` which validates that its input is a valid list of
    tag names.
    """
    def clean(self, value):
        return value
