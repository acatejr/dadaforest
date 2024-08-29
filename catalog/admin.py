from django.contrib import admin
from .models import SearchTerm

@admin.register(SearchTerm)
class SearchTermAdmin(admin.ModelAdmin):
    ordering = ["pk"]
    list_display = [
        "id",
        "term",
    ]

