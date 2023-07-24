from django.shortcuts import render, redirect
from .models import Question, Answer, Tag
from .forms import QuestionForm, AnswerForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from users.models import Users, Notification
from django.shortcuts import get_object_or_404
import os
# Create your views here.


def questions_list(request):
    questions = Question.objects.all().order_by('-created_at')
    query = request.GET.get('q')
    if query:
        questions = questions.filter(text__icontains=query)

    paginator = Paginator(questions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'QandA/mainpage.html', {'page_obj': page_obj})


def question_detail(request, pk,):
    question = Question.objects.get(pk=pk)
    best_answer = Answer.objects.filter(topic=question).exclude(rating__lte=0).order_by('-rating').first()
    if request.user.is_authenticated:
        Notification.objects.filter(user=request.user, question_id=pk).delete()
    if best_answer:
        answers = Answer.objects.filter(topic=question).exclude(id=best_answer.id).order_by('-rating')
    else:
        answers = Answer.objects.filter(topic=question).order_by('-rating')
    Answer.objects.filter(topic=question, rating__lt=-5).delete()
    if request.method == 'POST':
        if 'vote' in request.POST:
            answer_id = request.POST['answer_id']
            vote = request.POST['vote']
            answer = Answer.objects.get(id=answer_id)
            value = 1 if vote == 'up' else -1
            user_id = str(request.user.id)
            prev_value = answer.voters.get(user_id, 0)
            if prev_value != value:
                answer.voters[user_id] = value
                answer.rating += value - prev_value
                answer.save()
            return redirect('QnA:question_detail', pk=pk)
        else:
            form = AnswerForm(request.POST, request.FILES)
            if form.is_valid():
                answer = form.save(commit=False)
                user = Users.objects.get(user=request.user)
                answer.save()
                answer.topic.set([question])
                answer.commentator.add(user)
                answer.save()
                Notification.objects.create(user=question.author.user, question=question, answer=answer)
                return redirect('QnA:question_detail', pk=pk)
    else:
        form = AnswerForm()
    context = {
        'question': question,
        'answers': answers,
        'form': form,
        'best_answer': best_answer
    }
    return render(request, 'QandA/question_detail.html', context)


def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save(commit=False)
            user = Users.objects.get(user=request.user)
            question.author = user
            question.save()
            for tag in form.cleaned_data['genre']:
                question.genre.add(tag)
            return redirect('QnA:questions_list')
    else:
        form = QuestionForm()
    return render(request, 'QandA/question_form.html', {'form': form})


def tag_questions(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    questions = Question.objects.filter(genre=tag)
    context = {
        'tag': tag,
        'questions': questions
    }
    return render(request, 'QandA/tag_detail.html', context)


@login_required
def delete(request, pk):
    if request.method == 'POST':
        delete_type = request.POST.get('delete_type')
        if delete_type == 'question':
            # Delete question
            question = Question.objects.get(pk=pk)
            if request.user == question.author.user:
                # Delete uploaded files
                if question.image:
                    if os.path.isfile(question.image.path):
                        os.remove(question.image.path)
                if question.files:
                    if os.path.isfile(question.files.path):
                        os.remove(question.files.path)
                question.delete()
                return redirect('QnA:questions_list')
        elif delete_type == 'answer':
            # Delete answer
            answer_id = request.POST.get('answer_id')
            answer = Answer.objects.get(id=answer_id)
            if request.user == answer.commentator.first().user:
                # Delete uploaded files
                if answer.image:
                    if os.path.isfile(answer.image.path):
                        os.remove(answer.image.path)
                if answer.files:
                    if os.path.isfile(answer.files.path):
                        os.remove(answer.files.path)
                answer.delete()
        return redirect('QnA:question_detail', pk=pk)

