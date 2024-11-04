from django.contrib import admin

from .models import Question, SubjectCategoryMapping, Subjects, Answers

admin.site.register(Question)
admin.site.register(SubjectCategoryMapping)
admin.site.register(Subjects)
admin.site.register(Answers)
