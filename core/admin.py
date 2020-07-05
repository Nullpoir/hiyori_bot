from django.contrib import admin
from .models import *
from .forms import *
# Register your models here.

class QuizAdmin(admin.ModelAdmin):
    fields = ('question','answers','is_active')
    form = QuizAdminForm
    list_display = ('__str__','created_at','is_active','update_at',)
    list_filter = ('is_active','created_at','update_at')

class UserAdmin(admin.ModelAdmin):
    list_filter = ('is_active','created_at','update_at')
    list_display = ('__str__','created_at','is_active','update_at',)

admin.site.register(User,UserAdmin)
admin.site.register(Quiz,QuizAdmin)
