from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Participant, Page, PageRating

from .forms import ParticipantCreateForm, PageRatingCreateForm


class QuestionaireView(generic.edit.CreateView):
    model = Participant
    form_class = ParticipantCreateForm
    success_url = '/page_generator/start_page'
    template_name = 'page_generator/questionaire.html'

    def form_valid(self, form):
        object = form.save()
        self.request.session['participant'] = object.id
        self.request.session['round'] = 1
        if not self.request.session.session_key:
            self.request.session.save()
        form.instance.session_id = self.request.session.session_key
        return super(QuestionaireView, self).form_valid(form)


class StartView(generic.base.TemplateView):
    template_name = 'page_generator/start_page.html'

    def start(request):
        return HttpResponseRedirect('/page_generator/page')


class PageView(generic.ListView):
    model = Page
    template_name = 'page_generator/page.html'

    context_object_name = 'pages'

    def get_queryset(self):
        # get page parameters for actual participant accordind his id and page order
        participant_id = self.request.session['participant']
        order = self.request.session['round']
        pages = Page.objects.filter(participant=participant_id).filter(order=order)

        if pages.first():
            # set actual page to user session for next use in page rating
            self.request.session['page_id'] = pages.first().id
            # increase round for next use
            self.request.session['round'] = order+1

        return pages


class PageRatingView(generic.edit.CreateView):
    model = PageRating
    form_class = PageRatingCreateForm
    template_name = 'page_generator/page_rating.html'

    def form_valid(self, form):
        page = Page.objects.get(pk=self.request.session['page_id'])
        form.instance.page = page
        return super(PageRatingView, self).form_valid(form)

    def get_success_url(self):
        # set to value number of rounds + 1
        if self.request.session['round'] == 3:
            return reverse('page_generator:link_page')
        else:
            return reverse('page_generator:page')


class PageLinkView(generic.ListView):
    model = Participant
    template_name = 'page_generator/link_page.html'

    context_object_name = 'participants'

    def get_queryset(self):
        participant_id = self.request.session['participant']
        print(participant_id)
        participants = Participant.objects.filter(id=participant_id)

        print(participants)

        return participants

    def start(request):
        return HttpResponseRedirect('/page_generator/index')


class IndexView(generic.ListView):
    template_name = 'page_generator/index.html'
    model = Participant

# https://docs.google.com/forms/d/e/1FAIpQLSdfXlxtegjEVSWMXdJnUM1Iij2x5hCvRb1YjGvU3k3nFwRq0Q/viewform?usp=pp_url&entry.918932795=21
