from django import forms
from .models import URL


class URLForm (forms.ModelForm):
    class Meta:
        model = URL
        fields = ['raw_url', 'short_url']
        widgets = {
            'raw_url': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the original URL',
            }),
            'short_url': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the short URL',
                'size': 20,
            })
        }

    def __init__(self, *args, **kwargs):
        super(URLForm, self).__init__(*args, **kwargs)

        self.fields['raw_url'].label = 'Destination URL'
        self.fields['short_url'].label = 'Short URL'
        
        self.fields['raw_url'].required = True
        self.fields['short_url'].required = False

