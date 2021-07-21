from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import  View
from django.utils import timezone
from django.forms import formset_factory
from django.contrib.auth.models import User
import datetime as dt

from .forms import EventForm
from .models import Event, Participation, PartChoice, Categ
from wiki.models import Article, Display

def get_categ(slug):
    if slug != None:
        return Categ.objects.filter(slug=slug)
    else:
        return Categ.objects.all()

def query_events(slug):
    t0 = dt.datetime.combine(dt.datetime.today(), dt.time(0, 0, 0))
    return Event.objects.filter(categ__in=get_categ(slug)) \
        .filter(date__gte=timezone.make_aware(t0)) \
        .order_by('date')

def query_participation(user, events):
    # create participation objects if they do not exist for user-event combis
    participants = []
    girls = []
    boys = []
    divers = []
    for e in events:
        # can be done with get_or_create()
        try:
            party = Participation.objects.filter(event=e)
            # party = sorted(party, key=lambda p: p.part.pk)
            girls.append([p for p in party if p.person.profile.gender == "f"])
            boys.append([p for p in party if p.person.profile.gender == "m"])
            divers.append([p for p in party if p.person.profile.gender == "d"])
            participants.append(party)
            part = Participation.objects.get(event=e, person=user)
        except Participation.DoesNotExist:
            Participation(event=e, person=user).save()

    return Participation.objects.filter(event__in=events) \
        .filter(person=user), participants, girls, boys, divers
    
class IndexView(View):
    template_name = 'events/eventslist.html'
    info = {}

    def get(self, request, slug=None):
        events = query_events(slug)
        participation, participants, girls, boys, divers = query_participation(
            request.user, events)
        gcount = [[p for p in party if p.part.choice == "y"]
                  for party in girls]
        bcount = [[p for p in party if p.part.choice == "y"]
                  for party in boys]
        dcount = [[p for p in party if p.part.choice == "y"]
                  for party in divers]
                  
        self.info.update({"particip": [{
            "id":p.id,
            "event":p.event_id, 
            "person":p.person_id, 
            "part":p.part} for p in participation
        ]})
        # create form instances
        EventFormSet = formset_factory(EventForm, extra=0)

        # TODO: Problem. initial values are somehow not used. If I can manage
        # to get this to work, I should have fixed everything, including 
        forms = EventFormSet(initial=self.info["particip"])
    
        # get posts (filtered on site)
        posts = Article.objects\
            .filter(show_on_pages=Display.objects.get(name='events'))

        context = { 'posts':  posts,
                    'formset': forms,
                    'eventforms': zip(
                        events, forms, participants, girls, boys, divers,
                        gcount, bcount, dcount),
                    'user': request.user,
                    'categories': get_categ(None)}

        return render(request, self.template_name, context)

    def post(self, request):
        EventFormSet = formset_factory(EventForm, extra=0)
        participation = self.info["particip"]
        formset = EventFormSet(request.POST, initial=participation)
        if formset.is_valid():
            for form, p in zip(formset, participation):
                if form.is_valid():
                    if form.has_changed():
                        # TODO: problem because ID of participation is not added to the fucking participation
                        new_p = form.save(commit=False) 
                        new_p.pk = p["id"]
                        new_p.save()
                        
        return HttpResponseRedirect(reverse('events:index'))
