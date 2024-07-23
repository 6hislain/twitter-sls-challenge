from django.contrib import admin
from .models import User, Tweet


# Register your models here.
class TweetAdmin(admin.ModelAdmin):
    search_fields = ["text"]
    list_filter = ["created_at"]


admin.site.register(User)
admin.site.register(Tweet, TweetAdmin)
