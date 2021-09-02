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
    def __init__(self, *args, **kwargs):
    	# take encoder and decoder kwargs from which come from the json field of tagfield
 		# the FIELD baseclass of django does not accept encoder and decoder kwargs
    	kwargs.pop('encoder', None)
    	kwargs.pop('decoder', None)
    	super(TagField, self).__init__(**kwargs)

    def clean(self, value):
        return value
