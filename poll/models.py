from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    RADIO = 'RB'
    CHECKBOX = 'CB'
    TYPE_VARIANT_CHOICES = [
        (RADIO, 'Радиокнопка'),
        (CHECKBOX, 'Чекбокс'),
    ]
    title = models.CharField(max_length=264)
    image = models.ImageField(null=True, blank=True,
                              upload_to='questions_image/')
    type_variant = models.CharField(max_length=2, choices=TYPE_VARIANT_CHOICES,
                                    default=RADIO)

    def __str__(self):
        return self.title


class Answer(models.Model):
    title = models.CharField(max_length=128, null=True, blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 related_name='answer_in_question', null=True)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Block(models.Model):
    POLL = 'PL'
    TEST = 'TS'
    TYPE_BLOCK_CHOICES = [
        (POLL, 'Опросник'),
        (TEST, 'Тест'),
    ]
    type_block = models.CharField(max_length=2, choices=TYPE_BLOCK_CHOICES,
                                  default=TEST)
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    question_count = models.SmallIntegerField(default=0)
    date_begin = models.DateTimeField('Дата начала теста',
                                      default=timezone.now)
    date_end = models.DateTimeField('Дата окончания теста', blank=True,
                                    null=True)
    available = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class QuestionInBlock(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 related_name='question', null=True)
    block = models.ForeignKey(Block, on_delete=models.CASCADE,
                              related_name='block')
    weight = models.SmallIntegerField(editable=True, default=0)

    def __str__(self):
        return str(self.question)


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_in_block = models.ForeignKey(QuestionInBlock,
                                          on_delete=models.CASCADE,
                                          related_name='question_in_block')
    answers = models.ManyToManyField(Answer, related_name='answer')

    def __str__(self):
        return str(self.user)


class BlockResult(models.Model):
    block = models.ForeignKey(Block, on_delete=models.CASCADE,
                              related_name='result')
    result = models.SmallIntegerField(editable=True, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='block_result')
    is_full = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.block) + ' ' + str(self.result)
