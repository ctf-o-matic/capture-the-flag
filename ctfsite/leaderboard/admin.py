from django.contrib import admin
from django.utils.timezone import now

from leaderboard.models import Team, TeamMember, Level, Submission, Hint, Server, UserServer


class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 1


class SubmissionInline(admin.TabularInline):
    model = Submission
    extra = 1


class TeamAdmin(admin.ModelAdmin):
    inlines = (TeamMemberInline, SubmissionInline)


class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('team', 'user', 'created_at')
    list_filter = ('team', )


class HintInline(admin.TabularInline):
    model = Hint
    extra = 1


class LevelAdmin(admin.ModelAdmin):
    inlines = (HintInline,)


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('team', 'level', 'user', 'created_at')


class HintAdmin(admin.ModelAdmin):
    list_display = ('level', 'text', 'visible')
    list_filter = ('level', 'visible')

    actions = ['show_hints', 'hide_hints']

    def show_hints(self, request, queryset):
        queryset.update(visible=True, updated_at=now())
    show_hints.short_description = "Make selected hints visible"

    def hide_hints(self, request, queryset):
        queryset.update(visible=False, updated_at=now())
    hide_hints.short_description = "Make selected hints hidden"


class UserServerAdmin(admin.ModelAdmin):
    list_display = ('user', 'server')
    list_filter = ('server', )


admin.site.register(Team, TeamAdmin)
admin.site.register(TeamMember, TeamMemberAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Hint, HintAdmin)
admin.site.register(Server)
admin.site.register(UserServer, UserServerAdmin)
