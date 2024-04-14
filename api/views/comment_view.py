from django.shortcuts import redirect
from ..models import *
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone


@csrf_exempt
def add_comment(request, thread_id):
    print(f"Valor de thread_id: {thread_id}")
    thread = Publicacio.objects.get(pk=thread_id)
    if request.method == 'POST':
        body = request.POST.get('entry_comment[body]')
        if body:
            default_user = User.objects.get(username='default_user')
            comment = Comment(body=body, author=default_user, thread=thread, creation_data=timezone.now())
            comment.save()
    return redirect('veure_thread', thread_id=thread_id)


@csrf_exempt
def add_reply(request, thread_id, comment_id):
    comment_root = Comment.objects.get(pk=comment_id)
    thread = Publicacio.objects.get(pk=thread_id)
    if request.method == 'POST':
        body = request.POST.get('entry_comment[body]')
        if body:
            default_user = User.objects.get(username='default_user')
            comment_reply = Comment(body=body, author=default_user, thread=thread, creation_data=timezone.now(),
                                    level=comment_root.level + 1)
            comment_reply.save()
            reply = Reply(comment_root=comment_root, comment_reply=comment_reply)
            reply.save()
    return redirect('veure_thread', thread_id=thread.id)
