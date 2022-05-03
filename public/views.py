import datetime

from django.utils import timezone
from django.views import generic

from events.models import Categ, Event, PartChoice, Participation
from public.models import Info
from wiki.models import Article, Display


class IndexView(generic.ListView):
    model = Article
    template_name = "public/home.html"
    context_object_name = "home_public_posts"

    def get_context_data(self, **kwargs):
        welcome = Info.objects.get(id=1)
        home = Display.objects.get(name="home")
        posts = Article.objects.filter(show_on_pages=home)
        public_posts = posts.filter(visibility="public")
        published_posts = public_posts.filter(pub_date__lte=timezone.now())
        start_today = datetime.datetime.combine(datetime.datetime.today(), datetime.time(0, 0, 0))
        training = Categ.objects.get(name="training")
        yes = PartChoice.objects.filter(choicetext="yes")[0]
        next_trainings = (
            Event.objects.filter(categ=training).order_by("-date").filter(date__gte=timezone.make_aware(start_today))
        )
        if len(next_trainings) > 0:
            next_training = next_trainings[0]
            participants = next_training.participation_set.all()
            partn = sum([1 for p in participants if p.part == yes])
        else:
            next_training = {"date": "Sommer: Di/Do, 18 Uhr ATV; " "Winter: Mo/Do, 22 Uhr HTWK"}
            participants = None
            partn = 0

        context = {
            "welcome": welcome,
            "published_posts": published_posts,
            "next_training": next_training,
            "participants": participants,
            "partn": partn,
        }
        return context
