import datetime

from django.db import models
from django.utils import timezone


class Participant(models.Model):

    class GenderChoices(models.TextChoices):
        FEMALE = 'F', 'Žena'
        MALE = 'M', 'Muž'

    class AgeChoices(models.TextChoices):
        TEENS = 'T', '15-20'
        YOUNG = 'Y', '20-25'
        ADULTS_1 = 'A1', '25-35'
        ADULTS_2 = 'A2', '35-45'
        ADULTS_3 = 'A3', '45-55'
        ADULTS_4 = 'A4', '55-65'
        SENIORS = 'S', '65+'

    class EducationChoices(models.TextChoices):
        PRIMARY = '1', 'Základné'
        SECONDARY = '2', 'Stredoškolské bez maturity'
        SECONDARY_M = '3', 'Stredoškolské s maturitou'
        UNIVERSITY = '4', 'Vysokoškolské'
        NONE = '0', 'Žiadne'

    class ProfessionChoices(models.TextChoices):
        HEALTHCARE = 'H', 'Zdravotníctvo'
        EDUCATION = 'E', 'Školstvo'
        CONSTRUCTION = 'C', 'Stavbeníctvo'
        RESTAURANTS = 'R', 'Reštauračné služby'
        BUSINESS = 'B', 'Podnikanie'

    gender = models.CharField(
        max_length=7,
        choices=GenderChoices.choices,
        default=None,
    )
    age = models.CharField(
        max_length=10,
        choices=AgeChoices.choices,
        default=None,
    )
    education = models.CharField(
        max_length=50,
        choices=EducationChoices.choices,
        default=None,
    )
    student = models.BooleanField(default=False)
    profession = models.CharField(
        max_length=30,
        choices=ProfessionChoices.choices,
        default=None,
    )
    session_id = models.CharField(max_length=500)


class Page(models.Model):

    class ParameterChoices(models.IntegerChoices):
        CATEGORY_1 = '1'
        CATEGORY_2 = '2'
        CATEGORY_3 = '3'

    class ColorChoices(models.IntegerChoices):
        GROUP_1 = '1'
        GROUP_2 = '2'
        GROUP_3 = '3'
        GROUP_4 = '4'

    class StyleChoices(models.IntegerChoices):
        STYLE_1 = '1'
        STYLE_2 = '2'
        STYLE_3 = '3'
        STYLE_4 = '4'

    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    order = models.IntegerField()
    headline_size = models.IntegerField(
        choices=ParameterChoices.choices,
        default=None,
    )
    font_size = models.IntegerField(
        choices=ParameterChoices.choices,
        default=None,
    )
    font_style = models.IntegerField(
        choices=StyleChoices.choices,
        default=None,
    )
    image_count = models.IntegerField(
        choices=ParameterChoices.choices,
        default=None,
    )
    colors = models.IntegerField(
        choices=ColorChoices.choices,
        default=None,
    )
    text_length = models.IntegerField(
        choices=ParameterChoices.choices,
        default=None,
    )
    hyperlink_count = models.IntegerField(
        choices=ParameterChoices.choices,
        default=None,
    )


class PageRating(models.Model):

    class CredibilityChoices(models.IntegerChoices):
        UNCREDIBLE_3 = -3, 'Úplne nedôveryhodný'
        UNCREDIBLE_2 = -2, 'Dosť nedôveryhodný'
        UNCREDIBLE_1 = -1, 'Trochu nedôveryhodný'
        DONT_KNOW = 0, 'Neviem posúdiť'
        CREDIBLE_1 = 1, 'Trochu dôveryhodný'
        CREDIBLE_2 = 2, 'Dosť dôveryhodný'
        CREDIBLE_3 = 3, 'Úplne dôveryhodný'

    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    credibility = models.IntegerField(
        choices=CredibilityChoices.choices,
        default=None,
    )
    headline_length = models.BooleanField(default=False)
    headline_size = models.BooleanField(default=False)
    font_size = models.BooleanField(default=False)
    font_style = models.BooleanField(default=False)
    image_count = models.BooleanField(default=False)
    colors = models.BooleanField(default=False)
    text_length = models.BooleanField(default=False)
    hyperlink_count = models.BooleanField(default=False)
    page_layout = models.BooleanField(default=False)

