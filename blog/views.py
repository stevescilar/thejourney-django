from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView


# def post_list(request):
#     post_list = Post.published.all()
#     # pagination with 3 posts per page
#     paginator = Paginator(post_list, 3)  # instantiate the Paginator Class
#     page_number = request.GET.get("page", 1)  # retrieve page
#     try:
#         posts = paginator.page(page_number)

#     except PageNotAnInteger:
#         posts = paginator.page(1)

#     except EmptyPage:
#         # if page_number is out of range deliver last page of results
#         posts = paginator.page(paginator.num_pages)
#     return render(request, "blog/post/list.html", {"posts": posts})

# using class based views

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html" 

def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )

    return render(request, "blog/post/detail.html", {"post": post})
