from django import forms

from .models import Participant, PageRating


class ParticipantCreateForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['gender', 'age', 'education', 'student', 'profession']
        widgets = {
            'gender': forms.RadioSelect(),
            'age': forms.RadioSelect(),
            'education': forms.RadioSelect(),
            'profession': forms.RadioSelect(),
        }
        labels = {
            'gender': ('Pohlavie'),
            'age': ('Vek'),
            'education': ('Dosiahnuté vzdelanie'),
            'student': ('Ste študent?'),
            'profession': ('Oblasť profesie'),
        }


class PageRatingCreateForm(forms.ModelForm):
    class Meta:
        model = PageRating
        fields = '__all__'
        exclude = ['page', ]
        widgets = {
            'credibility': forms.RadioSelect(),
        }
        labels = {
            'credibility': ('Dôveryhodnosť'),
            'headline_length': ('Dĺžka nadpisu'),
            'headline_size': ('Veľkosť nadpisu'),
            'font_style': ('Štýl písma'),
            'font_size': ('Veľkosť písma'),
            'image_count': ('Počet obrázkov'),
            'colors': ('Farby použité na stránke'),
            'text_length': ('Dĺžka textu'),
            'hyperlink_count': ('Počet hypertextových odkazov'),
            'page_layout': ('Rozloženie elementov na stránke'),
        }
