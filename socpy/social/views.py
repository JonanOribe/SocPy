from dataclasses import field
from multiprocessing import context
import profile
from django.db.models import Q
from pyexpat import model
from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Comment, Post,UserProfile
from .forms import PostForm,CommentForm
from django.views.generic.edit import UpdateView,DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
class PostListView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        logged_in_user = request.user
        posts = Post.objects.filter(
            author__profile__followers__in=[logged_in_user.id]
        ).order_by('-created_on')
        form = PostForm()

        context = {
            'post_list': posts,
            'form': form,
        }

        return render(request, 'social/post_list.html', context)

    def post(self, request,*args, **kwargs):
        posts = Post.objects.all().order_by('-created_on')
        form = PostForm(request.POST)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()

        context = {
            'post_list': posts,
            'form': form,
        }
        
        return render(request,'social/post_list.html',context)

class PostDetailsView(LoginRequiredMixin,View):
    def get(self,request,pk,*args,**kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm()
        comments = Comment.objects.filter(post=post).order_by('-created_on')
        context = {
            'post':post,
            'form':form,
            'comments': comments
        }

        return render(request,'social/post_detail.html',context)

    def post(self,request,pk,*args,**kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

        comments = Comment.objects.filter(post=post).order_by('-created_on')
        context = {
            'post': post,
            'form': form,
            'comments': comments
        }

        return render(request,'social/post_detail.html',context)

class PostEditView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['body']
    template_name = 'social/post_edit.html'

    def get_success_url(self) -> str:
        pk = self.kwargs['pk']
        return reverse_lazy('post-detail', kwargs={'pk':pk})
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    template_name = 'social/post_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class CommentDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Comment
    template_name = 'social/comment_delete.html'

    def get_success_url(self) -> str:
        pk = self.kwargs['post_pk']
        return reverse_lazy('post-detail', kwargs={'pk':pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class ProfileView(View):
    def get(self,request,pk,*args,**kwargs):
        profile = UserProfile.objects.get(pk=pk)
        user = profile.user
        posts = Post.objects.filter(author=user).order_by('-created_on')

        followers = profile.followers.all()

        if len(followers)==0:
            is_following = False

        for follower in followers:
            if follower == request.user:
                is_following = True
                break
            else:
                is_following = False

        number_of_followers = len(followers)

        context = {
            'user':user,
            'profile': profile,
            'posts':posts,
            'number_of_followers':number_of_followers,
            'is_following':is_following
        }
        return render(request,'social/profile.html',context)

class CommentReplyView(LoginRequiredMixin,View):
    def post(self,request,post_pk,pk,*args,**kwargs):
        post = Post.objects.get(pk=pk)
        parent_comment = Comment.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author= request.user
            new_comment.post = post
            new_comment.parent = parent_comment
            new_comment.save()

        return redirect('post-detail', pk=post_pk)
class ProfileEditView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = UserProfile
    fields = ['name','bio','birth_date','location','picture']
    template_name= 'social/profile_edit.html'

    def get_success_url(self) -> str:
        return reverse_lazy('profile',kwargs={'pk':self.kwargs['pk']})

    def test_func(self):
        return self.request.user == self.get_object().user

class AddFollower(LoginRequiredMixin,View):
    def post(self, request,pk,*args,**kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.add(request.user)
        return redirect('profile',pk=profile.pk)

class RemoveFollower(LoginRequiredMixin,View):
    def post(self,request,pk,*args,**kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.remove(request.user)
        return redirect('profile',pk=profile.pk)

class AddLike(LoginRequiredMixin,View):
    def post(self,request,pk,*args,**kwargs):
        post = Post.objects.get(pk=pk)
        is_like = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                post.dislikes.remove(request.user)
                break

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        post.likes.remove(request.user) if is_like else post.likes.add(request.user)

        next = request.POST.get('next','/')
        return HttpResponseRedirect(next)
class AddDislike(LoginRequiredMixin,View):
    def post(self,request,pk,*args,**kwargs):
        post = Post.objects.get(pk=pk)
        is_dislike = False

        for like in post.likes.all():
            if like == request.user:
                post.likes.remove(request.user)
                break

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        post.dislikes.remove(request.user) if is_dislike else post.dislikes.add(request.user)

        next = request.POST.get('next','/')
        return HttpResponseRedirect(next)

class UserSearch(View):
    def get(self,request,*args,**kwargs):
        query = self.request.GET.get('query')
        profile_list = UserProfile.objects.filter(
            Q(user__username__icontains=query)
        )

        context = {
            'profile_list':profile_list
        }

        return render(request,'social/search.html',context)

class ListFollowers(View):
    def get(self,request,pk,*args,**kwargs):
        profile = UserProfile.objects.get(pk=pk)
        followers = profile.followers.all()

        context = {
            'profile':profile,
            'followers':followers
        }

        return render(request,'social/followers_list.html',context)

class AddCommentLike(LoginRequiredMixin,View):
    def post(self,request,pk,*args,**kwargs):
        comment = Comment.objects.get(pk=pk)
        is_like = False

        for dislike in comment.dislikes.all():
            if dislike == request.user:
                comment.dislikes.remove(request.user)
                break

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        comment.likes.remove(request.user) if is_like else comment.likes.add(request.user)

        next = request.POST.get('next','/')
        return HttpResponseRedirect(next)

class AddCommentDislike(LoginRequiredMixin,View):
    def post(self,request,pk,*args,**kwargs):
        comment = Comment.objects.get(pk=pk)
        is_dislike = False

        for like in comment.likes.all():
            if like == request.user:
                comment.likes.remove(request.user)
                break

        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        comment.dislikes.remove(request.user) if is_dislike else comment.dislikes.add(request.user)

        next = request.POST.get('next','/')
        return HttpResponseRedirect(next)
