from django.contrib import admin

from .models import Hunt, Problem, Team

# Register your models here.

admin.site.register(Hunt)
admin.site.register(Team)
admin.site.register(Problem)
