from unicodedata import name
from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name="index"),
    path('feed/',views.feed,name="feed"),
    path('<int:num>',views.sqd,name="sqd"),
    path('ask/',views.ask,name="ask"),
    path('add/<int:no>',views.ansadd,name="ansadd"),
    path('edit/<int:num>/<int:no>',views.editans,name="editans"),
    path('delete/<int:num>/<int:no>',views.deleteans,name="deleteans"),
    path('reply/<int:q_id>/<int:ans_id>',views.addreply,name="addreply"),
    path('reply_to/<int:q_id>/<int:ans_id>/<int:c_id>',views.add_reply,name="add_reply"),
    path('like_cnt/<int:id>',views.queslike,name="like"),
    path('dislike_cnt/<int:id>',views.quesdislike,name="dislike"),
    path('deleteques/<int:id>',views.deleteques,name="deleteques"),
    path('deletecomment/<int:id>/<int:no>',views.deletecomments,name="deletecomment"),
    path('deletereply/<int:id>/<int:no>',views.deletereply,name="deletereply"),
    path('bookmark/<int:id>',views.bookmark,name="bookmark"),
    path('profile/<int:id>',views.profile,name="profile"),
]
