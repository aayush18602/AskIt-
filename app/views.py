from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Question,Answer,QuesLikes,QuesDisLikes,BookMark,Moderator,Comment
from .forms import QuestionForm,AnswerForm,CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from simple_search import search_filter
from django.contrib import messages
from profanity_filter import ProfanityFilter
from bs4 import BeautifulSoup
# Create your views here.

pf = ProfanityFilter()

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
    return render(request,"app/sqd.html",{
        "ques":ques,
        "ans":ans,
        "ansfield":ansfield,
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
        raw_ans = request.POST['ans']
        # print(raw_ans)
        soup = BeautifulSoup(raw_ans,features="html.parser")
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        ansobj.ans_toques = getques
        ansobj.ans_askedby = request.user
        if pf.is_profane(text):
            print(1)
            ansobj.ans = raw_ans
            mod_obj = Moderator()
            ansobj.save()
            mod_obj.answer = ansobj
            mod_obj.save()
            messages.error(request,'Your answer contains some harmful words!! We are looking into it')
            return redirect(sqd,num=no)
        else:
            print(2)
            ansobj.ans = raw_ans
            ansobj.save()
        return redirect(sqd,num=no)

@login_required(login_url='/accounts/login')
def editans(request,num,no):
    ansfield = Answer.objects.filter(id=no).first()
    if request.user != ansfield.ans_askedby:
        return redirect(index)
    if(request.POST.get('hidval')):
        raw_ans = request.POST['ans']
        soup = BeautifulSoup(raw_ans,features="html.parser")
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        check = Moderator.objects.filter(answer=ansfield).first()
        if pf.is_profane(text):
            ansfield.ans = raw_ans
            ansfield.save()
            if check is None:
                prof = Moderator(answer=ansfield)
                prof.save()
                messages.error(request,'Your answer contains some harmful words!! We are looking into it')
            return redirect(sqd,num=num)
        else:
            ansfield.ans = raw_ans
            ansfield.save()
            if check is not None:
                check.delete()
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

@login_required(login_url='/accounts/login')
def moderator(request,del_st=None):
    if not request.user.is_superuser:
        return redirect(index)
    if request.method == 'POST':
        # print("Hiiii")
        st = request.GET['message']
        if st == 'delete':
            Answer.objects.filter(id=del_st).delete()
        elif st == 'remove':
            Moderator.objects.filter(id=del_st).delete()
        return redirect(moderator,del_st=0)
    ans = Moderator.objects.all()
    return render(request,'app/moderator.html',{
        "ans":ans
    })

@login_required(login_url='/accounts/login')
def display_ans(request,q_id,ans_id):
    ques = Question.objects.get(id=q_id)
    ans = Answer.objects.get(id=ans_id)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.user = request.user
            user_comment.c_ans = ans  
            user_comment.save()
            return redirect(display_ans,q_id=q_id,ans_id=ans_id)
    else:
        comment_form = CommentForm()
    comments = ans.get_comments.filter()
    return render(request,'app/answer.html',{
        "ques":ques,
        "sing":ans,
        "comments":comments,
        "comment_form":comment_form
    })

@login_required(login_url='/accounts/login')
def deletecomments(request,q_id,ans_id,c_id):
    if request.method == 'POST':
        check = Comment.objects.get(id=c_id).delete()
        return redirect(display_ans,q_id,ans_id)
    return redirect(index)