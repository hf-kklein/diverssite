from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import  View
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.forms import formset_factory
from django.contrib.auth.models import AnonymousUser, User
import datetime as dt
from .forms import EventForm
from .models import Event, Participation, Categ
from wiki.models import Article, Display
from users.models import Profile

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

def get_profile(party, gender):
    gender_list = []
    for p in party:
        try:
            profile = p.person.profile
        except ObjectDoesNotExist:
            profile = Profile(
                user=p.person,
                gender="d"
            )
            profile.save()

        if profile.gender == gender:
            gender_list.append(p)

    return gender_list

def get_user_or_anonymous(user):
    if not isinstance(user, AnonymousUser):
        return user

    try:
        anonymous = User.objects.get(username="anonymous")
    except User.DoesNotExist:
        anonymous = User(username="anonymous")
        anonymous.save()

    return anonymous


def query_participation(user, events):
    # create participation objects if they do not exist for user-event combis
    participants = []
    girls = []
    boys = []
    divers = []
    participation = []
    for e in events:
        # can be done with get_or_create()
        try:
            party = Participation.objects.filter(event=e)
            # party = sorted(party, key=lambda p: p.part.pk)
            girls.append(get_profile(party, "f"))
            boys.append(get_profile(party, "m"))
            divers.append(get_profile(party, "d"))
            participants.append(party)
            participation.append(Participation.objects.get(event=e, person=user))
        except Participation.DoesNotExist:
            Participation(event=e, person=user).save()

    # if isinstance(user, AnonymousUser):
        # participation = Participation.objects.none()
    # else:

        
    return participation, participants, girls, boys, divers


    
    
def present_on_parties(party_list):
    new_list = []
    for party in party_list:
        new_party = []
        for p in party:
            if p.part is None:
                pass
            elif p.part.choice == "y":
                new_party.append(p)

        new_list.append(new_party)
    
    return new_list

class IndexView(View):
    template_name = 'events/eventslist.html'

    def get(self, request, slug=None):
        events = query_events(slug)
        user = get_user_or_anonymous(request.user)
        participation, participants, girls, boys, divers = query_participation(
            user, events)
        gcount = present_on_parties(girls)
        bcount = present_on_parties(boys)
        dcount = present_on_parties(divers)
                  
        initial = ({"particip": [{
            "id":p.id,
            "event":p.event_id, 
            "person":p.person_id, 
            "part":p.part} for p in participation
        ]})
        # create form instances
        EventFormSet = formset_factory(EventForm, extra=0)

        # TODO: Problem. initial values are somehow not used. If I can manage
        # to get this to work, I should have fixed everything, including 
        forms = EventFormSet(initial=initial["particip"])
    
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
        # participation = self.info["particip"]
        formset = EventFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    if form.has_changed():
                        data = form.cleaned_data
                        participation_entry = Participation.objects.filter(
                            person=data["person"],
                            event=data["event"]
                        )
                        
                        assert len(participation_entry) == 1
                        participation = participation_entry[0]
                        participation.part = data["part"]
                        participation.save()
                        
        return HttpResponseRedirect(reverse('events:index'))
