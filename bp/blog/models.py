from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length = 200)
    pub_date = models.DateTimeField('data published')
    body = models.TextField()

    writer=models.ForeignKey(User, on_delete=models.CASCADE, null=True) #on_delete: 객체와의 연결을 끊을 때, 삭제할 때 사용. null=true: 빈 정보라도 괜찮다고 하는 것. false인 게 가장 좋음. 데이터가 꽉 차 있는게 좋다는 것.
    likes=models.ManyToManyField(User, through='Like', through_fields=('blog','user'), related_name="likes" ) #manytomany model 사용. like를 통과하는데 뭘 가지고 중계하느냐?=> user, likes로 중계모델을 둔다.
    

    def __str__(self):
        return self.title

class Comment(models.Model):
    body=models.TextField(max_length=500)
    pub_date=models.DateTimeField('data published')
    writer=models.ForeignKey(User, on_delete=models.CASCADE)
    post=models.ForeignKey(Blog, on_delete=models.CASCADE) #블로그 글 중 하나

class Like(models.Model):
    blog=models.ForeignKey(Blog, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE) #연결인데 foeignkey 쓴 이유=좋아요 입장이기 때문에 유저 한 개당 여러 개의 좋아요가 만들어질 수 있고 블로그에 대해서는 여러 유저들이 좋아요를 달 수 있기 때문에 like입장에서 user와 1대 다 모델을 형성.