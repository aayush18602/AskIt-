from turtle import mode
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel,TreeForeignKey


# Create your models here.
class Question(models.Model):
    title = models.CharField(max_length=300)
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="get_allques")
    created  = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = models.CharField(max_length=20,blank=True,null=True)
    like_count = models.IntegerField(default=0)
    dislike_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Answer(models.Model):
    ans = RichTextField()
    ans_askedby = models.ForeignKey(User,on_delete=models.CASCADE,related_name="quesasked")
    ans_toques = models.ForeignKey(Question,on_delete=models.CASCADE,related_name="ans_toques")
    like_count = models.IntegerField(default=0)
    dislike_count = models.IntegerField(default=0)
    created  = models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return f"Answer :- {self.id} :- {self.ans_toques} by {self.ans_askedby}"

class Comment(MPTTModel):
    content = models.CharField(max_length=100)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_commented")
    c_ans = models.ForeignKey(Answer,on_delete=models.CASCADE,related_name="get_comments")
    parent = TreeForeignKey('self',on_delete=models.CASCADE,related_name='children',null=True,blank=True)
    added = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
        order_insertion_by = ['added']
    def __str__(self):
        return f"Comment by {self.user.id}"


    
    
class QuesLikes(models.Model):
    ques = models.ForeignKey(Question,on_delete=models.CASCADE)
    likeuser = models.ForeignKey(User,on_delete=models.CASCADE)

class QuesDisLikes(models.Model):
    ques = models.ForeignKey(Question,on_delete=models.CASCADE)
    dislikeuser = models.ForeignKey(User,on_delete=models.CASCADE)

class BookMark(models.Model):
    ques = models.ForeignKey(Question,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="get_bookmarks")

    def __str__(self):
        return f"{self.ques.id} :- {self.user}"


class Moderator(models.Model):
    answer = models.ForeignKey(Answer,related_name="mod_ans",on_delete=models.CASCADE)
