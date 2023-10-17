from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from .models import Question, Choice
from django.db.models import QuerySet
from django.urls import reverse
from django.views import generic
from django.utils import timezone

# def details(request: HttpRequest) -> JsonResponse:
#     data = {
#         'id': 1,
#         'class': 'Django',
#         'language': 'Python'
#     }
#     return JsonResponse(data)

# Create your views here.

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
            :5
        ]
    
# def index(request: HttpRequest) -> HttpResponse:
#     latest_question_list: QuerySet[Question] = Question.objects.order_by("pub_date")[:5]
#     # output: list[str] = ", ".join([q.question_text for q in latest_question_list])
#     context = {
#         "latest_question_list": latest_question_list,
#     }
#     return render(request, 'polls\index.html', context)

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/details.html"

# def detail(request: HttpRequest, question_id: int) -> HttpResponse:
#     question = get_object_or_404(Question, id=question_id)
#     return render(request, 'polls/details.html', {'question':question})

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

# def results(request: HttpResponse, question_id: int) -> HttpResponse:
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/results.html", {"question": question})


def vote(request: HttpRequest, question_id: int) -> HttpResponse:
    question: Question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/details.html', {
            'question':question,
            'error_message': "You didn't select a choice."
            })
    else:
        # Database is lazy
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))