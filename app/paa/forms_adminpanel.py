from django import forms
from .models_adminpanel import SystemSettings
from .models_import import ImportProfile


class BrandingForm(forms.ModelForm):
    class Meta:
        model = SystemSettings
        fields = ["branding", "colors"]


class FeatureFlagsForm(forms.ModelForm):
    class Meta:
        model = SystemSettings
        fields = ["feature_flags"]


class SMTPTestForm(forms.Form):
    email = forms.EmailField()


class ImportProfileForm(forms.ModelForm):
    class Meta:
        model = ImportProfile
        fields = "__all__"
