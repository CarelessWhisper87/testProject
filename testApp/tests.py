from django.test import TestCase
from django.contrib.auth.models import User 
from .models import Post
class PostModelTest(TestCase): 
    def test_str_representation(self): 
    # 1. Arrange (準備) 
        # テスト用のユーザーと投稿を作成
        user = User.objects.create_user(username='testuser', password='password') 
        post = Post.objects.create(author=user, content='This is a test post that is very long.')
        # 2. Act (実行)
    # __str__メソッドを呼び出す
    str_output = str(post)
    # 3. Assert (検証)
    # 期待通りの文字列になっているかを確認
    self.assertEqual(str_output, 'testuser: This is a test post...')
