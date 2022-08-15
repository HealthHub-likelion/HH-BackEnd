from django.contrib import admin
from .models import Exercise,Routine,RoutineExercise,Set
# Register your models here.
admin.site.register(Exercise)
admin.site.register(Routine)
admin.site.register(RoutineExercise)
admin.site.register(Set)
