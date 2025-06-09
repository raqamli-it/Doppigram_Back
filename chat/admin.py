from django.contrib import admin
from .models import Chat, Message


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'created')
    filter_horizontal = ('participants',)
    search_fields = ('participants__username',)
    ordering = ('-created',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat', 'sender', 'type', 'created')
    list_filter = ('type', 'created')
    search_fields = ('content', 'sender__username', 'chat__id')
    ordering = ('-created',)