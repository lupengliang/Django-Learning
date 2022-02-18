from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Note


def check_login(fn):
    def warp(request, *args, **kwargs):
        if 'username' not in request.session or 'uid' not in request.session:
            # 检查Cookies
            c_username = request.COOKIES.get('username')
            c_uid = request.COOKIES.get('uid')
            if not c_username or not c_uid:
                return HttpResponseRedirect('user/login')
            else:
                # 回写session
                request.session['username'] = c_username
                request.session['uid'] = c_uid
        return fn(request, *args, **kwargs)
    return warp

# Create your views here.
@check_login
def add_note(request):

    if request.method == 'GET':
        return render(request, 'note/add_note.html')
    elif request.method == 'POST':
        # 处理数据
        uid = request.session['uid']
        title = request.POST['title']
        content = request.POST['content']
        link = request.POST['link']

        Note.objects.create(title=title, content=content, user_id=uid, link=link)
        return HttpResponseRedirect(reverse('note:show_note'))


# 删除笔记
def delete_note(request):
    note_id = request.GET.get('note_id')
    if not note_id:
        return HttpResponse('--请求异常')
    try:
        note = Note.objects.get(id=note_id)
    except Exception as e:
        print('---delete note get error %s' % (e))
        return HttpResponse('---The note id is error')
    # 伪删除 － 即更新操作
    # 这里因为数据不重要用的是真正的删除
    note.delete()
    return HttpResponseRedirect(reverse('note:show_note'))  # reverse自己了解下


# 更新笔记
def update_note(request, note_id):
    try:
        note = Note.objects.get(id=note_id)
    except Exception as e:
        print('--update note error is %s' % (e))
        return HttpResponse('--The note is note existed.')
    if request.method == 'GET':
        return render(request, 'note/update_note.html', locals())
    elif request.method == 'POST':
        print('提前成功')
        content = request.POST['content']
        link = request.POST['link']
        note.content = content  # 更新内容
        note.link = link  # 更新内容
        note.save()  # 进行保存

    return HttpResponseRedirect(reverse('note:show_note'))


# 查看笔记
def show_note(request):
    all_notes = Note.objects.all()
    return render(request, 'note/all_note.html', {'all_notes': all_notes})


