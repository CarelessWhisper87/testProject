from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from .models import Post 
from .serializers import PostSerializer
import requests

 # DRFのジェネリックビューをインポート
from rest_framework import generics
 #Postモデルの一覧を返す、API専門のクラスベースビュー
@login_required # ログインしていないといいねできないようにする
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    if post.likes.filter(id=user.id).exists():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True
    context = {
        'liked': liked,  # 今の状態（いいねしたのか、外したのか）
        'count': post.total_likes(), # 最新のいいね数
    }
    # JsonResponseを使ってJSON形式で返却
    return JsonResponse(context)

class PostListAPIView(generics.ListAPIView): 
# どのデータの一覧を返すか
    queryset = Post.objects.all() 
# どの翻訳者（シリアライザ）を使ってJSONに変換するか
    serializer_class = PostSerializer
class SignUpView(CreateView): 
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def timeline(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(content__icontains=query).order_by('-created_at')
    else:
        posts = Post.objects.select_related('author').order_by('-created_at')

    context = {
        'posts': posts,
        'query': query,
    }
    return render(request, 'timeline.html', context)


def post_detail(request, pk):
    # 指定されたpk（主キー）のPostオブジェクトを取得
    post = get_object_or_404(Post, pk=pk)
    # テンプレートに該当の投稿データを渡して表示
    return render(request, 'post_detail.html', {'post': post})


@login_required
def post_create(request):
    if request.method == 'POST':
        # リクエストされたPOSTデータからフォームを作成
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # ログイン中のユーザーを著者に設定
            post.save()
            return redirect('timeline')
    else:
        # GETリクエストの場合、空のフォームを表示
        form = PostForm()
    return render(request, 'post_create.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # 投稿者とログインユーザーが一致しない場合はリダイレクト
    if request.user != post.author:
        return redirect('post_detail', pk=pk)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'post_edit.html', {'form': form, 'post': post})


def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # 投稿者とログインユーザーが一致しない場合はリダイレクト
    if request.user != post.author:
        return redirect('post_detail', pk=pk)

    if request.method == 'POST':
        post.delete()
        return redirect('timeline')
    return render(request, 'post_confirm_delete.html', {'post': post})




def dog_view(request):
    api_url = 'https://dog.ceo/api/breeds/image/random'
    response = requests.get(api_url)
    data = response.json()

    context = {
        'dog_image': data['message'],
        'status': data['status'],
    }

    return render(request, 'dog.html', context)
