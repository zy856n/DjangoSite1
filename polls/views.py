from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice


# # def index(request):
# #     # Displays the latest 5 poll questions
# #     latest_question_list = Question.objects.order_by('-pub_date')[:5]
# #     output = '<br/>'.join([q.question_text for q in latest_question_list])
# #     return HttpResponse(output)


# # def index(request):
# #     # Displays the latest 5 poll questions
# #     latest_question_list = Question.objects.order_by('-pub_date')[:5]
# #     template = loader.get_template("polls/index.html")
# #     context = {
# #         'latest_question_list': latest_question_list,
# #     }
# #     return HttpResponse(template.render(context, request))


# def index(request):
#     # Re-rewritten
#     latest_question_list = Question.objects.order_by('-pub_date')[0:10]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'polls/index.html', context)


# # def details(request, question_id):
# #     # Details of a poll
# #     try:
# #         question = Question.objects.get(pk=question_id)
# #     except Question.DoesNotExist:
# #         raise Http404("Question does not exist.")
# #     return render(request, 'polls/details.html', {'question':question})


# def details(request, question_id):
#     # Details of a poll
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/details.html', {'question': question})


# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last ten published questions. Exclude the ones to be published in the future
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[0:10]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/details.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    # ...
    question = get_object_or_404(Question, pk=question_id)
    
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/details.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))