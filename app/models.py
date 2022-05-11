from turtle import mode
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


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


class Comment(models.Model):
    content = models.TextField()
    ans_ref = models.ForeignKey(Answer,related_name="getallreplies",on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name="getalluser_toreply",on_delete=models.CASCADE)
    ques_ref = models.ForeignKey(Question,related_name="reply_toques",on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f"Comment :- {self.user} to answer id: {self.ans_ref.id}"

class Reply(models.Model):
    content = models.TextField()
    ans_ref = models.ForeignKey(Answer,related_name="getallans",on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name="getall_user_toreply",on_delete=models.CASCADE)
    ques_ref = models.ForeignKey(Question,related_name="to_which_ques",on_delete=models.CASCADE,null=True)
    comment_ref = models.ForeignKey(Comment,related_name="reply_towhich_comment",on_delete=models.CASCADE)

    def __str__(self):
        return f"Reply to {self.ques_ref.id}, Answer: {self.ans_ref.id} Comment {self.comment_ref.id}"
    
    
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