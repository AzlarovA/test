from django.contrib import admin
from .models import Question, Answer, Tag
# Register your models here.


class QuestionAdmin(admin.ModelAdmin):
    list_display = ("title", "author", 'content')
    list_display_links = ("title", "author", 'content')


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('content',)
    list_display_links = ('content',)


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Tag)