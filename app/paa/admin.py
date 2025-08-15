from django.contrib import admin
from .models import Plan, Action, ActionPlan


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "mode", "owner", "is_active")
    search_fields = ("code", "name")
    list_filter = ("mode", "is_active")


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ("code", "title", "status", "priority", "due_date", "j_delta")
    search_fields = ("code", "title", "description")
    list_filter = ("status", "priority")
    filter_horizontal = ("responsables",)


@admin.register(ActionPlan)
class ActionPlanAdmin(admin.ModelAdmin):
    list_display = ("action", "plan")
    search_fields = ("action__code", "plan__code")
