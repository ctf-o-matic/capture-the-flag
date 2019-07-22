from django.contrib import admin

from leaderboard.models import Team, TeamMember, Level, Submission


class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 1


class SubmissionInline(admin.TabularInline):
    model = Submission
    extra = 1


class TeamAdmin(admin.ModelAdmin):
    inlines = (TeamMemberInline, SubmissionInline)


class LevelAdmin(admin.ModelAdmin):
    pass


class SubmissionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Team, TeamAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(Submission, SubmissionAdmin)
