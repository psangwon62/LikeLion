from datetime import time
from django.core.checks import messages
from django.http import request
from django.shortcuts import render,get_object_or_404,redirect
from .models import Blog, Comment
from django.utils import timezone
# Create your views here.
def blog(request):
    blogs = Blog.objects.all()
    return render(request,'blog.html', { 'blogs' : blogs })

def detail(request, blog_id):
    detail = get_object_or_404(Blog, pk=blog_id)
    comments=Comment.objects.all().filter(post=detail) #post와 detail이 같을 때 그것과 관련된 모든 것을 filter해서 가져오는 것.
    #likes=>순서쌍('현재 blog.id',  '현재 user.id')
    #이 순서쌍이 LIke모델에 있다면 좋아요를 누른 것! -> 좋아요 취소 message를 전달
    #이 순서쌍이 like모델에 없다면 좋아요를 누르지 않은 것! => 좋아요 message 전달
    if detail.likes.filter(id=request.user.id):
        message="좋아요 취소"
    else:
        message="좋아요"
    return render(request ,'detail.html', { 
        'detail' : detail, 
        'comments':comments, 
        'message':message
        } )


def new(request):
    return render(request, 'new.html')

def create(request):
    blog = Blog() # 객체 틀 하나 가져오기
    blog.title = "NoTitle"  # 내용 채우기
    if request.GET['title']:
        blog.title=request.GET['title']
    blog.body = request.GET['body'] # 내용 채우기
    blog.pub_date = timezone.datetime.now() # 내용 채우기
    blog.writer=request.user
    blog.save() # 객체 저장하기

    # 새로운 글 url 주소로 이동
    return redirect('/blog/' + str(blog.id))

#삭제
def delete(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    blog.delete()
    return redirect('/blog/')
#update

def update(request, blog_id):
    blog = get_object_or_404(Blog, pk =blog_id)

    if request.method == "POST":
        if request.POST['title']:
            blog.title=request.POST['title']
        blog.body = request.POST['body']
        blog.pub_date = timezone.datetime.now()
        blog.save()
        return redirect('/blog/' +str(blog.id))
    else:
        return render(request,'update.html')

def comment(request, blog_id):
    if request.method=="POST":
        comment = Comment()
        comment.body=request.POST['body']
        comment.pub_date=timezone.datetime.now()
        comment.writer=request.user
        comment.post=get_object_or_404(Blog, pk=blog_id)
        comment.save()
        return redirect('/blog/'+str(blog_id))
    else: return redirect('/blog/'+str(blog_id))

def comment_delete(request, comment_id):
    comment=get_object_or_404(Comment, pk=comment_id)
    blog_id=comment.post.id
    comment.delete()

    return redirect('/blog/'+str(blog_id))

#like관련 함수
def post_like(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    user=request.user

    if blog.likes.filter(id=user.id):
        blog.likes.remove(user) #if문에서 있다면 현재 유저와 맞는 것을 remove 없다면 add
    else: blog.likes.add(user)

    return redirect('/blog/'+str(blog_id))