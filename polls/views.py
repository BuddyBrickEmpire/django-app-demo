from django import forms
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from . import models


class QuestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['answer'].empty_label = None
        self.fields['answer'].queryset = models.Choice.objects.filter(question=self.instance.question)

    class Meta:
        model = models.Response
        fields = ['answer']
        widgets = {
            'answer': forms.RadioSelect
        }


class PollView(View):

    def get(self, request):
        question_id = request.GET.get('id')
        if question_id:
            try:
                question = models.Question.objects.get(pk=question_id)
                return render(request, 'detail.html', {
                    'form': QuestionForm(instance=models.Response(question=question)),
                    'question': question,
                })
            except models.Question.DoesNotExist:
                return HttpResponse(status=404)

        return render(request, 'index.html', {
            'latest_question_list': models.Question.objects.all()[:5]
        })

    def post(self, request):
        question_id = request.GET.get('id')
        if question_id:
            try:
                question = models.Question.objects.get(pk=question_id)
                form = QuestionForm(instance=models.Response(question=question), data=request.POST)
                if form.is_valid():
                    form.save()
                    return redirect(reverse('index'))
                else:
                    return render(request, 'detail.html', {
                        'form': form,
                        'question': question,
                    })
            except models.Question.DoesNotExist:
                return HttpResponse(status=404)

        return self.get(request)

