from django import forms
from django.contrib.auth.models import User
from .models import Membre

class MembreForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, label='Prénom')
    last_name = forms.CharField(max_length=30, required=True, label='Nom')
    email = forms.EmailField(required=True, label='Email')
    username = forms.CharField(max_length=150, required=True, label='Nom d\'utilisateur')
    password = forms.CharField(widget=forms.PasswordInput(), required=False, label='Mot de passe')
    
    class Meta:
        model = Membre
        fields = ['date_naissance', 'telephone', 'adresse']
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
            self.fields['username'].initial = self.instance.user.username
            self.fields['username'].widget.attrs['readonly'] = True
            self.fields['password'].required = False
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if not self.instance.id:  # Nouveau membre
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError("Ce nom d'utilisateur est déjà pris.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if not self.instance.id:  # Nouveau membre
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("Cet email est déjà utilisé.")
        return email
    
    def save(self, commit=True):
        if self.instance.id:  # Modification
            user = self.instance.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            if self.cleaned_data['password']:
                user.set_password(self.cleaned_data['password'])
            user.save()
            membre = super().save(commit=commit)
        else:  # Création
            user = User.objects.create_user(
                username=self.cleaned_data['username'],
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name']
            )
            membre = super().save(commit=False)
            membre.user = user
            if commit:
                membre.save()
        
        return membre 