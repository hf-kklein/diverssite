from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic, View
from django.utils import timezone
from django.contrib.auth.models import User
import json

from .models import Event, Participation, PartChoice
from public.models import Post



class IndexView(View):
    def get(self, request):
        current_user = request.user
        # print(current_user, current_user.id)
        event_query = Event.objects.filter().order_by('date')
        posts = Post.objects.filter(page = 'events')
        parti = Participation.objects.all()
        parti_user = parti.filter(person = current_user.id)
        choices_query = PartChoice.objects.all()
        yes = PartChoice.objects.get(choice = 'y')



        events = dict()
        for event in event_query:
            participation_all = event.participation_set.all()
            part_count = len(participation_all.filter(part = yes))
            try:
                participation_user = event.participation_set.get(person = current_user).part.choicetext
            except:
                participation_user = None

            choices = dict()
            for i in choices_query:
                choices[i.choice] = {'choicetext': i.choicetext,
                                     'userchoice': participation_user}

            events[event.id] = {'event': event,
                                'participation_all': participation_all,
                                'participation_count': part_count,
                                'participation_user': participation_user,
                                'choices': choices}

        context = { 'posts':  posts,
                    # 'events': event_query,
                    'events': events,
                    'user': current_user}

        print(context)
        return render(request, 'events/index.html', context)

    def post(self, request):
        # print(request.POST)

        def nest_dict(flat):
            result = {}
            for k, v in flat.items():
                _nest_dict_rec(k, v, result)
            return result

        def _nest_dict_rec(k, v, out):
            k, *rest = k.split('_', 1)
            if rest:
                _nest_dict_rec(rest[0], v, out.setdefault(k, {}))
            else:
                out[k] = v

        data = nest_dict(request.POST.dict())
        try:
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

        except (KeyError):
            evlist = dict()
            print("no choices were updated")



        return HttpResponseRedirect(reverse('events:index'))
    # try:
    #     event = event.get(id=request.POST['event'])


#
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(request, 'polls/detail.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         }
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
# #
# class DetailView(generic.DetailView):
#     model = Event
#     template_name = 'events/detail.html'
#     def get_queryset(self):
#         """
#         Excludes any questions that aren't published yet.
#         """
#         return Event.objects.filter(pub_date__lte=timezone.now())



# class ResultsView(generic.DetailView):
#     model = Question
#     template_name = 'polls/results.html'
#
