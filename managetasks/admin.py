from django.contrib import admin
from mapwidgets.widgets import GooglePointFieldWidget

from .models import *

class CityAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget}
    }

admin.site.register(PointsCore,CityAdmin)
