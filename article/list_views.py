from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 
from .models import ArticleColumn, ArticlePost, Comment
from .forms import CommentForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import Count

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

import redis
from django.conf import settings
r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)



def article_titles(request, username=None):
    if username:
        user = User.objects.get(username=username)
        articles_title = ArticlePost.objects.filter(author=user)
        try:
            userinfo = user.userinfo
            userprofile = user.userprofile
        except:
            userinfo = None
            userprofile = None
    else:
        articles_title = ArticlePost.objects.all()
    paginator = Paginator(articles_title, 5)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list 
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list 
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages) 
        articles = current_page.object_list
    
    if username:
        return render(request, "article/list/author_articles.html", {"articles":articles, "page":current_page, "userinfo":userinfo, "user":user,"userprofile":userprofile})
    return render(request, "article/list/article_titles.html", {"articles":articles, "page": current_page})

# @login_required(login_url='/account/login/')
def article_detail(request, id, slug):
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    total_views = r.incr("article:{}:views".format(article.id))
    r.zincrby('article_ranking', 1, article.id)

    article_ranking = r.zrange("article_ranking", 0, -1, desc=True)[:10]
    article_ranking_ids = [int(id) for id in article_ranking]
    most_viewed = list(ArticlePost.objects.filter(id__in=article_ranking_ids))
    most_viewed.sort(key=lambda x: article_ranking_ids.index(x.id))
# 评论
#     user_id = request.session.get('_auth_user_id')
#     user = User.objects.get(id=user_id)
#     print("用户名："+user.username)
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        # comment_form.commentator = request.user.username
        if comment_form.is_valid():
            if request.user.is_authenticated:
                username = request.user.username
                print("用户名：" + username)

                new_comment = comment_form.save(commit=False)
                new_comment.commentator = username
                new_comment.user = request.user
                new_comment.article = article
                new_comment.save()
            else:
                return HttpResponseRedirect(reverse("account:user_login"))
    else:
        comment_form = CommentForm()


    article_tags_ids = article.article_tag.values_list("id", flat=True)
    similar_articles = ArticlePost.objects.filter(article_tag__in=article_tags_ids).exclude(id=article.id)
    similar_articles = similar_articles.annotate(same_tags=Count("article_tag")).order_by('-same_tags', '-created')[:4]
    return render(request, "article/list/article_content.html", {"article":article, "total_views":total_views, "most_viewed": most_viewed, "comment_form":comment_form, "similar_articles":similar_articles})
    # return render(request, "article/list/article_content.html", {"article":article, "total_views":total_views, "most_viewed": most_viewed, "comment_form":comment_form})

@csrf_exempt
@require_POST
@login_required(login_url='/account/login/')
def like_article(request):
    article_id = request.POST.get("id")
    action = request.POST.get("action")
    if article_id and action:
        try:
            article = ArticlePost.objects.get(id=article_id)
            if action=="like":
                article.users_like.add(request.user)
                return HttpResponse("1")
            else:
                article.users_like.remove(request.user)
                return HttpResponse("2")
        except:
            return HttpResponse("no")


@login_required(login_url='/account/login/')
@require_POST
@csrf_exempt
def comment_delete(request):
    comment_id = request.POST["comment_id"]
    print(comment_id)
    try:
        line = Comment.objects.get(id=comment_id)
        line.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")