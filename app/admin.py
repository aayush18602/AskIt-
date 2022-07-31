from django.contrib import admin

# Register your models here.
from .models import QuesDisLikes, Question,Answer,QuesLikes,BookMark,Moderator,Comment
from mptt.admin import MPTTModelAdmin

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(QuesLikes)
admin.site.register(QuesDisLikes)
admin.site.register(BookMark)
admin.site.register(Moderator)
admin.site.register(Comment,MPTTModelAdmin)