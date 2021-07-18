from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic, View
from django.utils import timezone
from django.forms import formset_factory
from django.contrib.auth.models import User
import json
import datetime as dt

from .forms import EventForm
from .models import Event, Participation, PartChoice, Categ
from wiki.models import Article, Display

class EventsViewOld(View):
    """
    add some standard methods to all views related to events.
    """
    def nest_dict(self,flat):
        result = {}
        for k, v in flat.items():
            self._nest_dict_rec(k, v, result)
        return result

    def _nest_dict_rec(self,k, v, out):
        k, *rest = k.split('_', 1)
        if rest:
            self._nest_dict_rec(rest[0], v, out.setdefault(k, {}))
        else:
            out[k] = v

    def create_events_dict(self):
        # print(self.cats)
        start_today = datetime.datetime.combine(datetime.datetime.today(), datetime.time(0, 0, 0))
        subset_events = Event.objects.filter(categ__in=self.cats)
        event_query = subset_events.filter(date__gte=timezone.make_aware(start_today)).order_by('date')
        choice_query = PartChoice.objects.all()
        choice_yes = PartChoice.objects.get(choice = 'y')
        choice_no = PartChoice.objects.get(choice = 'n')
        choice_maybe = PartChoice.objects.get(choice = 'm')

        events = dict()
        for event in event_query:
            participation_all = event.participation_set.all()
            participation_yes = participation_all.filter(part = choice_yes)
            participation_no = participation_all.filter(part = choice_no)
            participation_maybe = participation_all.filter(part = choice_maybe)
            part_count = len(participation_all.filter(part = choice_yes))
            try:
                participation_user = event.participation_set.get(person = self.user_query).part.choicetext
            except:
                participation_user = None

            choices = dict()
            for i in choice_query:
                choices[i.choice] = {'choicetext': i.choicetext,
                                     'userchoice': participation_user}

            events[event.id] = {'event': event,
                                'participation_all': participation_all,
                                'participation_yes': participation_yes,
                                'participation_no': participation_no,
                                'participation_maybe': participation_maybe,
                                'participation_count': part_count,
                                'participation_user': participation_user,
                                'choices': choices}


        return events

    def process_participation(self, data):
        evlist = data["evlist"]
        print(evlist)
        for u in evlist:
            for ev in evlist[u]:
                use = User.objects.get(username=u)
                print(use)
                eve = Event.objects.get(pk=ev)
                cho = PartChoice.objects.get(choice=evlist[u][ev][0])
                p = Participation.objects.filter(person=use)
                p = p.filter(event=eve)
                if len(p) == 0:
                    pnew = Participation(
                        event = eve,
                        person = use,
                        part = cho
                        )
                    pnew.save()
                elif len(p) == 1:
                    p.update(part=cho)
                else:
                    print("error. Too many events selected.")
                    break

def get_categ(slug):
    if slug != None:
        return Categ.objects.filter(slug=slug)
        # print(cat)
        # self.cats = self.allcats.filter(categ=sel_cat)
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
    for e in events:
        # can be done with get_or_create()
        try:
            participants.append(Participation.objects.filter(event=e))
            part = Participation.objects.get(event=e, person=user)
        except Participation.DoesNotExist:
            Participation(event=e, person=user).save()

    return Participation.objects.filter(event__in=events) \
        .filter(person=user), participants
    
class IndexView(View):
    template_name = 'events/eventslist.html'
    info = {}

    def get(self, request, slug=None):
        events = query_events(slug)
        participation, participants = query_participation(request.user, events)
        particount = [len(p) for p in participants]
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
                    'eventforms': zip(events, forms, participants, particount),
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
