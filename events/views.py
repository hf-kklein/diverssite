from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic, View
from django.utils import timezone
from django.contrib.auth.models import User
import json
import datetime

from .models import Event, Participation, PartChoice, Categ
from wiki.models import Article, Display


class EventsView(View):
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
        subset_events = Event.objects.filter(categ__in=self.cats)
        event_query = subset_events.filter(date__gte=datetime.date.today()).order_by('date')
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


class IndexView(EventsView):
    template_name = 'events/eventslist.html'



    def get(self, request, slug = None):
        self.allcats = Event.objects.values('categ')
        # print(self.cats)
        if slug != None:
            sel_cat = Categ.objects.get(slug=slug)
            print(sel_cat)
            self.cats = self.allcats.filter(categ=sel_cat)
        else:
            self.cats = self.allcats
        # with self make variable to class attribute, accessible to all methods
        # print(self.cats)
        self.user_query = request.user
        posts = Article.objects.filter(show_on_pages = Display.objects.get(name = 'events'))
        public_posts = posts.filter(visibility = 'public')
        member_posts = posts.filter(visibility = 'member')
        post_query = public_posts
        events = self.create_events_dict()


        context = { 'posts':  post_query,
                    'events': events,
                    'user': self.user_query,
                    'categories': self.allcats}
        return render(request, self.template_name, context)

    def post(self, request):
        data = self.nest_dict(request.POST.dict())
        try:
            self.process_participation(data)

        except (KeyError):
            evlist = dict()
            print("no choices were updated")

        return HttpResponseRedirect(reverse('events:index'))
