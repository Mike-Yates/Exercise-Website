from django.shortcuts import render
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'exercise/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
            Return the last five published questions.
        """
        return
