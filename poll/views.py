from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse_lazy
from django.utils import timezone

from poll.models import *


@login_required
def rating(request):
    template = loader.get_template('ratings.html')
    users = User.objects.all()
    s = 0
    for i in users:
        for j in i.block_result.all():
            s += j.result
        i.res = s
        s = 0
    context_dict = {
        'users': users
    }
    return HttpResponse(template.render(context_dict, request))


def index(request):
    return render(request, 'index.html')


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            auth.login(request, form.get_user())
            return HttpResponseRedirect(reverse_lazy('list_of_blocks_url'))
        else:
            return HttpResponseRedirect(reverse_lazy('login'))
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse_lazy('login'))


def start_redirect(request):
    return redirect('index', permanent=True)


def blocks_view(request):
    if request.user.is_authenticated:
        block_list = []
        for i in Block.objects.all():
            if not i.result.filter(user=request.user):
                block_list.append(i)
        template = loader.get_template('list_of_blocks.html')
        for i in block_list:
            if i.date_begin > timezone.now():
                i.available = False
                i.save()
            else:
                i.available = True
                i.save()
        context_dict = {
            "block_list": block_list
        }
        return HttpResponse(template.render(context_dict, request))
    else:
        return redirect('index')


@login_required
def block_detail(request, block_id):
    if request.user.is_authenticated:
        template = loader.get_template('block_detail.html')
        block = Block.objects.get(id=block_id)
        questions_in_block = QuestionInBlock.objects.filter(block__id=block_id)
        context_dict = {
            "all_questions": questions_in_block,
            "current_block": block
        }
        return HttpResponse(template.render(context_dict, request))
    else:
        return redirect('login')


def completed_block_list(request):
    block_list = []
    for i in Block.objects.all():
        try:
            if i.result.filter(user=request.user):
                i.res = i.result.get(user=request.user).result
                block_list.append(i)
        except TypeError:
            return HttpResponseRedirect(reverse_lazy('login'))
    template = loader.get_template('completed_tests.html')
    context_dict = {
        "block_list": block_list
    }
    return HttpResponse(template.render(context_dict, request))


@login_required
def finish_test(request, block_id):
    if request.POST.keys():
        template = loader.get_template('test_result.html')
        user_answers = request.POST.items()
        current_block = Block.objects.get(id=block_id)
        counter = 0
        amount = 0
        for i in user_answers:
            if counter == 0:
                counter += 1
                continue
            else:
                current_question = QuestionInBlock.objects.get(id=i[0][6:])
                current_answers = Answer.objects.filter(id=i[1])
                UserAnswer.objects.create(user=request.user,
                                          question_in_block=current_question)
                cur = UserAnswer.objects.get(user=request.user,
                                             question_in_block=current_question)
                cur.answers.set(current_answers)
                if current_answers[0].correct:
                    amount += current_question.weight
        BlockResult.objects.create(user=request.user, block=current_block,
                                   result=amount)
        res = BlockResult.objects.get(user=request.user, block=current_block,
                                      result=amount)
        res.is_completed = True
        res.save()
        result = BlockResult.objects.get(user=request.user, block=current_block,
                                         result=amount)
        max_point = QuestionInBlock.objects.filter(block=current_block).aggregate(
            Sum('weight'))
        context_dict = {
            "result": result,
            "max_point": max_point['weight__sum']
        }
        return HttpResponse(template.render(context_dict, request))
    else:
        return redirect('list_of_blocks_url')


@login_required
def finish_interview(request, block_id):
    if request.POST.keys():
        user_process_answers = {}
        user_answers_keys = list(request.POST.keys())[1:]
        for i in user_answers_keys:
            user_process_answers[i] = request.POST.getlist(i)
        current_block = Block.objects.get(id=block_id)
        for i in user_process_answers:
            current_question = QuestionInBlock.objects.get(id=i[6:])
            current_answers = []
            for j in Answer.objects.all():
                if j.id in list(map(int, user_process_answers[i])):
                    current_answers.append(j)
            UserAnswer.objects.create(user=request.user,
                                      question_in_block=current_question)
            cur = UserAnswer.objects.get(user=request.user,
                                         question_in_block=current_question)
            cur.answers.set(current_answers)
        BlockResult.objects.create(user=request.user, block=current_block)
        res = BlockResult.objects.get(user=request.user, block=current_block)
        res.is_completed = True
        res.save()
        return render(request, 'test_result.html')
    else:
        return redirect('list_of_blocks_url')
