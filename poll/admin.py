from django.contrib import admin

from poll.models import *


class QuestionInBlockInline(admin.TabularInline):
    model = QuestionInBlock
    extra = 0


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    fields = ['title', 'type_block', 'description', 'available', 'date_begin',
              'date_end', 'question_count']
    inlines = [QuestionInBlockInline]


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'type_variant')
    inlines = [AnswerInline]


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    pass


@admin.register(BlockResult)
class BlockResultAdmin(admin.ModelAdmin):
    pass
