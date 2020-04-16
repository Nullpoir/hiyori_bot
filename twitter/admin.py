from django.contrib import admin
from .forms import TalkSetAdminForm
from .models import TalkSet
# Register your models here.

class TalkSetAdmin(admin.ModelAdmin):
    form = TalkSetAdminForm

admin.site.register(TalkSet,TalkSetAdmin)
