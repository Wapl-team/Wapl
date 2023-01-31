from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http.request import HttpRequest

from server.apps.wapl.models import Comment


# Create your views here.

def main(request:HttpRequest,*args, **kwargs):
    return render(request, "main.html")


def comment(request:HttpRequest, *args, **kwargs):
    
    if request.method == "POST":
        Comment.objects.create(
            content=request.POST["content"],
            user=request.POST["user"],
            plan_post=request.POST["plan_post"],
        )
        return redirect('wapl:comment') 
    
    comments = Comment.objects.all()
    
    context = {
        "comments" : comments,
    }
    
    return render(request, "test__comment.html", context=context)

def comment_delete(request:HttpRequest, pk, *args, **kwargs):
    if request.method == "POST":
        comment = Comment.objects.get(id=pk)
        comment.delete()
    return redirect('wapl:comment')

