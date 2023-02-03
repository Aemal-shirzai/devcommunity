from django.contrib import admin

from .models import Project, Review, Tag

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "is_published", 'tags_count', 'update_date')
    list_display_links = ("title", )
    search_fields = ('title', 'owner__first_name')
    list_filter = ("owner", 'tags')

    actions = ['make_published', 'make_unpublished']
    date_hierarchy = 'create_date'
    empty_value_display = '-empty-'

    # By default, applied filters are preserved on the list view after creating, editing, 
    # or deleting an object. You can have filters cleared by setting this attribute to False.
    preserve_filters = False


    @admin.action(description='Publish')
    def make_published(self, request, queryset):
        queryset.update(is_published=True)

    @admin.action(description='Un Publish')
    def make_unpublished(self, request, queryset):
        queryset.update(is_published=False)

    def tags_count(self, obj):
        return obj.tags.count()

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("value", "project", 'owner')
    search_fields = ('value', )
    list_filter = ('value', "owner", 'project')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", )
    search_fields = ("name", )