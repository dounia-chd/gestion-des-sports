from django import forms
from .models import Sport, Niveau, Horaire

class SportForm(forms.ModelForm):
    class Meta:
        model = Sport
        fields = ['nom', 'description', 'niveau_requis', 'capacite_max', 'duree_seance', 'prix', 'image', 'actif']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'prix': forms.NumberInput(attrs={'min': 0, 'step': 0.01}),
            'capacite_max': forms.NumberInput(attrs={'min': 1}),
            'duree_seance': forms.NumberInput(attrs={'min': 15, 'step': 15}),
            'image': forms.FileInput(attrs={'accept': 'image/*'}),
        }
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024:  # 5MB max
                raise forms.ValidationError("L'image ne doit pas dépasser 5MB.")
            if not image.content_type.startswith('image/'):
                raise forms.ValidationError("Le fichier doit être une image.")
        return image 

class HoraireForm(forms.ModelForm):
    class Meta:
        model = Horaire
        fields = ['jour', 'heure_debut', 'heure_fin']
        widgets = {
            'heure_debut': forms.TimeInput(attrs={'type': 'time'}),
            'heure_fin': forms.TimeInput(attrs={'type': 'time'}),
        } 