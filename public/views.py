from django.views import generic
from django.utils import timezone
from datetime import date

from wiki.models import Articles, Display
from events.models import Event, Categ, Participation, PartChoice


class IndexView(generic.ListView):
    model = Articles
    template_name = 'public/home.html'
    context_object_name = 'home_public_posts'

    def get_context_data(self, **kwargs):
        welcome_title = "Saxy Divers Ultimate Frisbee"
        welcome_text = "Saxy Divers spielen seit 1990 Ultimate Frisbee in Leipzig"
        home = Display.objects.get(name = 'home')
        posts = Articles.objects.filter(show_on_pages = home)
        public_posts = posts.filter(visibility = 'public')
        published_posts = public_posts.filter(pub_date__lte=timezone.now())
        today = date.today()
        training = Categ.objects.get(name='training')
        yes = PartChoice.objects.filter(choicetext='yes')[0]
        next_trainings = Event.objects.filter(categ=training).order_by('-date').filter(date__gte=today)
        if len(next_trainings) > 0:
            next_training = next_trainings[0]
            participants = next_training.participation_set.all()
            partn = sum([1 for p in participants if p.part == yes])
        else:
            next_training = {'date': "Sommer: Di/Do, 18 Uhr ATV; "
                                     "Winter: Mo/Do, 22 Uhr HTWK"}
            participants = None
            partn = 0



        context = {'welcome_title': welcome_title,
                   'welcome_text': welcome_text,
                   'published_posts': published_posts,
                   'next_training': next_training,
                   'participants': participants,
                   'partn':partn
                   }
        return context





