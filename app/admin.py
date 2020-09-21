from django.contrib import admin
from app.models import *
from app.forms import *
# Register your models here.

class QuizAdmin(admin.ModelAdmin):
    fields = ('question','answers','is_active')
    form = QuizAdminForm
    list_display = ('__str__','created_at','is_active','update_at',)
    list_filter = ('is_active','created_at','update_at')

class UserAdmin(admin.ModelAdmin):
    list_filter = ('is_active','created_at','update_at')
    list_display = ('__str__','created_at','is_active','update_at',)

class TalkSetAdmin(admin.ModelAdmin):
    fields = ('name','trigger_body','reply')
    form = TalkSetAdminForm

admin.site.register(TalkSet,TalkSetAdmin)
admin.site.register(User,UserAdmin)
admin.site.register(Quiz,QuizAdmin)
