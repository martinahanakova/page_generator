from django.db.models.signals import post_save
from django.db.models import Count, Q
from django.contrib.sessions.backends.db import SessionStore
from django.dispatch import receiver

from .models import Participant, Page

import numpy as np
import math


@receiver(post_save, sender=Participant, dispatch_uid='participant_updated')
def generateParameters(sender, instance, created, **kwargs):
    rounds = 5
    if not created:

        for round in range(rounds):
            participant = instance
            order = round + 1
            headline_size = generate(participant, 'headline_size')
            font_size = generate(participant, 'font_size')
            font_style = generate(participant, 'font_style')
            image_count = generate(participant, 'image_count')
            colors = generate(participant, 'colors')
            text_length = generate(participant, 'text_length')
            hyperlink_count = generate(participant, 'hyperlink_count')

            page = Page(participant=participant,
                order=order,
                headline_size=headline_size,
                font_size=font_size,
                font_style=font_style,
                image_count=image_count,
                colors=colors,
                text_length=text_length,
                hyperlink_count=hyperlink_count)

            page.save()


def generate(participant, parameter):

    if participant.age == "T" or participant.age == "Y":
        age = "A1"
    elif participant.age == "A4" or participant.age == "S":
        age = "A3"
    else:
        age = "A2"

    if participant.education == "4":
        education = "E3"
    elif participant.education == "3" or participant.education == "2":
        education = "E2"
    else:
        education = "E1"

    if participant.student:
        student = "S"
    else:
        student = "NS"

    ageProbability = getProbability(age, parameter)
    educationProbability = getProbability(education, parameter)
    studentProbability = getProbability(student, parameter)

    allProbabilities = ageProbability * educationProbability * studentProbability

    array_sum = math.fsum(allProbabilities)
    normalized = allProbabilities / array_sum

    choices = Page._meta.get_field(parameter).choices

    values = []

    for value in choices:
        values.append(value[0])

    item = np.random.choice(values, p=normalized)

    return item


def getProbability(category, parameter):

    choices = Page._meta.get_field(parameter).choices

    values = {}

    for value in choices:
        values[value[0]] = 0

    if category == "A1":
        parameter_counts = Page.objects.values(parameter).\
        filter(participant__in=Participant.objects.filter(Q(age='T') | Q(age='Y'))).\
        annotate(Count(parameter))
    if category == "A2":
        parameter_counts = Page.objects.values(parameter).\
        filter(participant__in=Participant.objects.filter(Q(age='A1') | Q(age='A2') | Q(age='A3'))).\
        annotate(Count(parameter))
    if category == "A3":
        parameter_counts = Page.objects.values(parameter).\
        filter(participant__in=Participant.objects.filter(Q(age='A4') | Q(age='S'))).\
        annotate(Count(parameter))
    if category == "E1":
        parameter_counts = Page.objects.values(parameter).\
        filter(participant__in=Participant.objects.filter(Q(education='0') | Q(education='1'))).\
        annotate(Count(parameter))
    if category == "E2":
        parameter_counts = Page.objects.values(parameter).\
        filter(participant__in=Participant.objects.filter(Q(education='2') | Q(education='3'))).\
        annotate(Count(parameter))
    if category == "E3":
        parameter_counts = Page.objects.values(parameter).\
        filter(participant__in=Participant.objects.filter(Q(education='4'))).\
        annotate(Count(parameter))
    if category == "S":
        parameter_counts = Page.objects.values(parameter).\
        filter(participant__in=Participant.objects.filter(Q(student=True))).\
        annotate(Count(parameter))
    if category == "NS":
        parameter_counts = Page.objects.values(parameter).\
        filter(participant__in=Participant.objects.filter(Q(student=False))).\
        annotate(Count(parameter))

    sum = 0
    probabilities = []

    for value in parameter_counts:
        sum = sum + value[parameter + '__count']
        values[value[parameter]] = value[parameter + '__count']

    values = np.array(list(values.values()))

    if sum == 0:
        sum = 0.0000000001

    for value in values:
        probabilities.append(round(abs((value / sum) - 1), 2))

    array_sum = math.fsum(probabilities)
    probabilities = np.array(probabilities)
    normalized = probabilities / array_sum

    return normalized
