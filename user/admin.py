from django.contrib import admin

from .models import Profile, Skill, Message

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", 'user', 'location')
    search_fields = ("first_name", "last_name", "location")
    list_filter = ('location', )

    def full_name(self, obj):
        return obj.full_name

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', "sender", 'receiver', 'is_read')
    search_fields = ("subject", )
    list_filter = ('is_read', 'email', 'sender', 'receiver')


admin.site.register(Skill)

