from django.contrib import admin

# Register your models here.
from .models import QuesDisLikes, Question,Answer,Comment,Reply,QuesLikes,BookMark

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(QuesLikes)
admin.site.register(QuesDisLikes)
admin.site.register(BookMark)