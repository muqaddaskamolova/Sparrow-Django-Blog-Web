from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.forms import UserChangeForm


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title',
                  'content',
                  'photo',
                  'category',)

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Post Content'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            })

        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('title',
                  'technology',
                  'description',
                  'image',
                  'author',)

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Title'
            }),

            'technology': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Technology'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Description'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Author'
            })

        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username:', max_length=16, help_text="Max 16 symbols",
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Username'
                               }))
    password = forms.CharField(label='Password:', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your Password'
    }))


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your Password'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Submit Password'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your name'
        }))
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your surname'
        }))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your email address'
        }))
    birthday = forms.DateTimeField(widget=forms.DateTimeInput(attrs={
        'class': 'form-control',
        'placeholder': 'Birthday'
    }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'birthday', 'password1', 'password2')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widget = {
            'text': forms.Textarea(attrs={'class': 'form-control',
                                          'placeholder': 'Add Comment',
                                          'rows': 3,
                                          'style': 'border:none, border-bottom: 1px solid #ddd;'
                                          })
        }

class EditUserForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',

    }))
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',

        }))
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',

        }))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',

        }))

    class Meta:
        exclude = ('user', 'reference_number',)


def clean_username(self):
    username = self.cleaned_data['username']
    try:
        User.objects.get(username=username)
    except User.DoesNotExist:
        return username
    raise forms.ValidationError('That username is already taken, please select another.')


def clean_email(self):
    email = self.cleaned_data['email']
    try:
        User.objects.get(email=email)
    except User.DoesNotExist:
        return email
    raise forms.ValidationError('That email address is already in the database, please provide another.')


class CustomUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Since the pk is set this is not a new instance
            self.fields['username'] = self.instance.username
            self.fields['username'].widgets.attrs['readonly'] = True
