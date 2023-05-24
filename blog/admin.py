from django.contrib import admin
from .models import Category, Post, Developer, Project, Like, Comment


# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'title',
                    'category',
                    'views',
                    'created_at',
                    'updated_at',
                    'publish')
    list_display_links = ('title',)
    list_editable = ('publish',)
    readonly_fields = ('views',)
    list_filter = ('title', 'category', 'created_at',)


class DeveloperAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'full_name',
                    'job',
                    'phone',
                    )
    list_display_links = ('full_name',)
    list_filter = ('job',)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title',
                    'author',
                    'technology',

                    )
    list_display_links = ('title',)
    list_filter = ('title', 'author', 'technology')


admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Developer, DeveloperAdmin)
admin.site.register(Project, ProjectAdmin)
