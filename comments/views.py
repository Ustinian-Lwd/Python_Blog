from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from Lwd.models import UserInfo, ArticleInfo
from comments.models import Comment


# 文章评论
def article_comment(request, pk):
    # 当用户点击发表评论的时候
    article_com = get_object_or_404(ArticleInfo, pk=pk)

    if request.method == 'POST':
        token = request.session.get('token')
        user_to = UserInfo.objects.get(u_token=token)

        # 实例化评论
        com = Comment()
        # 评论内容
        com.com_content = request.POST.get('comment-text')
        #
        com.com_user = user_to
        #
        com.com_article = article_com
        # 评论加1
        article_com.a_comment_num += 1
        article_com.save()

        com.save()

        return HttpResponseRedirect(reverse('lwd:blog_detail',args={pk}))
    # 直接渲染出评论
    else:
        comment_list = article_com.comment_set.all()
        context = {'article': article_com,
                   'comment_list': comment_list
                   }
        return redirect(reverse('lwd:blog_detail', args={pk}), context=context)


# 删除评论
def delete_comment(request, pk):
    # token
    token = request.session.get("token")
    user_token = UserInfo.objects.filter(u_token=token)
    if user_token:
        user_token = user_token[0]
        comment_0 = Comment.objects.get(pk=pk)
        comment_0.delete()

        return HttpResponseRedirect(reverse('lwd:user_home', args={user_token.u_id}))

    # else:
    #     return HttpResponseRedirect(reverse('lwd:index'))



