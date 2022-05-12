from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Question,Answer,Comment,Reply,QuesLikes,QuesDisLikes,BookMark
from .forms import QuestionForm,AnswerForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from simple_search import search_filter
from django.contrib import messages
# Create your views here.

def index(request):
    return render(request,'app/index.html')

@login_required(login_url='/accounts/login')
def feed(request):
    form = QuestionForm()
    if request.GET.get('q'):
        q = request.GET['q']
        # allq = Question.objects.filter(title__search=q)
        fields = ['title']
        allq = Question.objects.filter(search_filter(fields,q))
    else:
        allq = Question.objects.all().order_by('-updated')
        q = None
    return render(request,"app/feed.html",{
        "qna":allq,
        "form":form,
        "q":q,
    })

@login_required(login_url='/accounts/login')
def sqd(request,num):
    ques = Question.objects.filter(id=num).first()
    ansfield = AnswerForm()
    if ques is None:
        print("Not found")
    ans = ques.ans_toques.all()
    all_reply = ques.reply_toques.all()
    all_replies = ques.to_which_ques.all()
    print(all_replies)
    return render(request,"app/sqd.html",{
        "ques":ques,
        "ans":ans,
        "ansfield":ansfield,
        "all_reply":all_reply,
        "replies":all_replies
    })

@login_required(login_url='/accounts/login')
def ask(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['qtitle']
            author = request.user
            tags = request.POST.get('tags',"")
            check = Question(title=title,author=author,tags=tags)
            check.save()
            return redirect(feed)

@login_required(login_url='/accounts/login')
def ansadd(request,no):
    if request.method == 'POST':
        getques = Question.objects.filter(id=no).first()
        ansobj = Answer()
        if request.POST['ans'] == "":
            messages.error(request,'Cannot add empty answer')
            return redirect(sqd,num=no)
        ansobj.ans = request.POST['ans']
        ansobj.ans_toques = getques
        ansobj.ans_askedby = request.user
        ansobj.save()
        return redirect(sqd,num=no)

@login_required(login_url='/accounts/login')
def editans(request,num,no):
    ansfield = Answer.objects.filter(id=no).first()
    if request.user != ansfield.ans_askedby:
        return redirect(index)
    if(request.POST.get('hidval')):
        ansfield.ans = request.POST['ans']
        ansfield.save()
        return redirect(sqd,num=num)
    ansform = AnswerForm(instance=ansfield)
    return render(request,"app/editans.html",{
        "ansform":ansform
    })

@login_required(login_url='/accounts/login')
def deleteans(request,num,no):
    ansfield = Answer.objects.filter(id=no).first()
    if request.user != ansfield.ans_askedby:
        return redirect(index)
    if ansfield is None:
        return redirect(index)
    ansfield.delete()
    return redirect(sqd,num=num)

@login_required(login_url='/accounts/login')
def addreply(request,q_id,ans_id):
    if request.method == "POST":
        comm_obj = Comment()
        comm_obj.content = request.POST['reply']
        ans = Answer.objects.get(id=ans_id)
        ques = Question.objects.get(id=q_id)
        comm_obj.ans_ref = ans
        comm_obj.ques_ref = ques
        comm_obj.user = request.user
        comm_obj.save()
        return redirect(sqd,num=q_id)


@login_required(login_url='/accounts/login')
def add_reply(request,q_id,ans_id,c_id):
    if request.method == "POST":
        rep_obj = Reply()
        ans = Answer.objects.get(id=ans_id)
        ques = Question.objects.get(id=q_id)
        comm = Comment.objects.get(id=c_id)
        rep_obj.content = request.POST['get_reply']
        rep_obj.ans_ref = ans
        rep_obj.ques_ref = ques
        rep_obj.user = request.user
        rep_obj.comment_ref = comm
        rep_obj.save()
        return redirect(sqd,num=q_id)

@login_required(login_url='/accounts/login')
def queslike(request,id):
    if request.method == 'POST':
        obj = Question.objects.get(id=id)
        check = QuesLikes.objects.filter(ques=obj,likeuser=request.user).first()
        if check is None:
            check2 = QuesDisLikes.objects.filter(ques=obj,dislikeuser=request.user).first()
            if check2 is not None:
                obj.dislike_count -=1
                check2.delete()
            obj.like_count +=1
            obj.save()
            newobj = QuesLikes(ques=obj,likeuser=request.user)
            newobj.save()
        else:
            check.delete()
            obj.like_count -=1
            obj.save()
        return redirect(feed)

@login_required(login_url='/accounts/login')
def quesdislike(request,id):
    if request.method == 'POST':
        obj = Question.objects.get(id=id)
        check = QuesDisLikes.objects.filter(ques=obj,dislikeuser=request.user).first()
        if check is None:
            check2 = QuesLikes.objects.filter(ques=obj,likeuser=request.user).first()
            if check2 is not None:
                obj.like_count -=1
                check2.delete()
            obj.dislike_count +=1
            obj.save()
            newobj = QuesDisLikes(ques=obj,dislikeuser=request.user)
            newobj.save()
        else:
            check.delete()
            obj.dislike_count -=1
            obj.save()
        return redirect(feed)

@login_required(login_url='/accounts/login')
def deleteques(request,id):
    if request.method == 'POST':
        check = Question.objects.get(id=id)
        check.delete()
        return redirect(feed)

def deletecomments(request,id,no):
    if request.method == 'POST':
        check = Comment.objects.get(id=id)
        check.delete()
        return redirect(sqd,num=no)

def deletereply(request,id,no):
    if request.method == 'POST':
        check = Reply.objects.get(id=id)
        check.delete()
        return redirect(sqd,num=no)


def bookmark(request,id):
    if request.method == 'POST':
        obj = Question.objects.get(id=id)
        check = BookMark.objects.filter(ques=obj,user=request.user).first()
        print("1")
        if check is None:
            newobj = BookMark(ques=obj,user=request.user)
            newobj.save()
        return redirect(feed) 

@login_required(login_url='/accounts/login')
def profile(request,id):
    user = User.objects.get(id=id)
    allques = user.get_allques.all()
    mess = True
    if request.method == 'POST':
        method = request.POST.get('Q')
        if method == 'B':
            allques = []
            test = user.get_bookmarks.all()
            for x in test:
                allques.append(Question.objects.get(id=x.ques.id))
        elif method == 'C':
            allques = []
            test = user.getalluser_toreply.all().values('ques_ref').distinct()
            for x in test:
                allques.append(Question.objects.get(id=x['ques_ref'])) 
        elif method == 'A':
            allques = []
            test = user.quesasked.all().values('ans_toques').distinct()
            print(test)
            for x in test:
                allques.append(Question.objects.get(id=x['ans_toques']))
        else:
            allques = user.get_allques.all()
        # if method == 'B':
        #     allques = []
        #     test = user.get_bookmarks.all()
        #     for x in test:
        #         allques.append(Question.objects.get(id=x.ques.id))
        #     mess = False
        # else:
        #     allques = user.get_allques.all()
    return render(request, 'app/profile.html',{
        "user":user,
        "allques": allques,
        "mess":mess
    })