from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Event, Participation
from public.models import Post



def index(request):
    if request.method == 'GET':
        current_user = request.user
        print(current_user, current_user.id)
        events = Event.objects.filter().order_by('date')
        posts = Post.objects.filter(page = 'events')
        parti = Participation.objects.all()
        parti_user = parti.filter(participants = current_user.id)
        print(parti, parti_user)
        context = { 'posts':  posts,
                    'events': events,}

        return render(request, 'events/index.html', context)

    if request.method == 'POST':
        print(request.POST)
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
