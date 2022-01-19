from django.contrib import admin
from django.db.models import fields
from .models import Answer, Profile, Question, UserAnswer
from import_export.admin import ImportExportModelAdmin
from import_export import resources
# Register your models here.



@admin.register(Profile)
class ProfileAdmin(ImportExportModelAdmin):
    pass


@admin.register(Question)
class QuestionAdmin(ImportExportModelAdmin):
    pass

@admin.register(Answer)
class AnswerAdmin(ImportExportModelAdmin):
    pass

@admin.register(UserAnswer)
class UserAnswerAdmin(ImportExportModelAdmin):
    pass

