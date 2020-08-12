from django import forms
from .models import User, UserProfileInfo


class UserForm(forms.ModelForm):
    # password1 = forms.CharField(max_length=256, widget=forms.PasswordInput(
    #     attrs={'class': 'form-control', 'placeholder': 'Enter Password'}), label='Password')
    password2 = forms.CharField(max_length=256, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Password Again'}), label='Re-enter Password')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'})
        }

    def clean(self):
        all_cleaned_data = super().clean()
        pass1 = all_cleaned_data['password']
        pass2 = all_cleaned_data['password2']

        if pass1 != pass2:
            raise forms.ValidationError('Passwords did not match')
        return self.cleaned_data


def url_check(value):
    if value[:8] != 'https://' and value[:7] != 'http://':
        raise forms.ValidationError(
            'Invalid URL. Include "https://" or "http://"')


class UserProfileInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfileInfo
        fields = ['portfolio_site', 'profile_pic']
        validators = [url_check]
        widgets = {
            'portfolio_site': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Portfolio Site'}),
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'})
        }
        labels = {
            'portfolio_site': 'Port-Folio Site',
            'profile_pic': 'Profile Photo',
        }
