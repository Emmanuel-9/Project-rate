from django.shortcuts import render, redirect, reverse
from .models import Post, Comment, Rating
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework import viewsets, permissions
from .serializers import PostSerializer, CommentSerializer,ProfileSerializer,UserSerializer
from .forms import RatingForm,ProfileUpdateForm,SignUpForm,UserUpdateForm,UserCreationForm
from django.views.generic.edit import FormMixin
from django.contrib.auth.models import User
import math
from .models import Post,Profile,Comment,Rating



# Create your views here.
def index(request):
    
    all_posts = Post.get_all_posts()
    context = {
        'posts': all_posts,
    }
    return render(request, 'welcome.html', context)

@method_decorator(login_required, name='dispatch')
class PostDetailView(FormMixin, DetailView):
    model = Post
    template_name = 'projects/post_detail.html'
    form_class = RatingForm

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        ratings = Rating.get_all_ratings(self.get_object())
        design = 0
        content = 0
        usability = 0
        for rating in ratings:
            design += rating.design
            content += rating.content
            usability += rating.usability        
        
        try:
            context['design'] = math.ceil(design/len(ratings))
            context['usability'] = math.ceil(usability/len(ratings))
            context['content'] = math.ceil(content/len(ratings))
        except:
            context['design'] = design
            context['usability'] = usability
            context['content'] = content
        
        context['ratings'] = len(ratings)
        context['form'] = RatingForm(initial={'post': self.object})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.post = self.get_object()
        form.instance.user = self.request.user        
        form.save()
        
        return super(PostDetailView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class PostCreateView(CreateView):
    model = Post
    fields = ['title','url','tech_used','desc', 'image_url']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class PostUpdateView(UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','url','desc', 'image_url']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False

@method_decorator(login_required, name='dispatch')
class PostDeleteView(UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False

@login_required
def add_comment(request, post_id):
    post = Post.objects.filter(pk=post_id)
    all_posts = Post.get_all_posts()   
    context = {
        'posts': all_posts,
        'post:': post
    }
    if request.method == 'POST':
        content = request.POST.get('comment')
        comment_inst = Comment(content=content, post_id=post_id)      
        comment_inst.save()  
        return redirect('welcome')
        
    return render(request, 'index.html', context)
        

@login_required
def add_like(request, post_id):
    post = Post.objects.filter(pk=post_id).first()
    post.likes += 1
    post.save()
    all_posts = Post.get_all_posts()   
    context = {
        'posts': all_posts,
    }    
        
    return render(request, 'index.html', context)

@login_required
def search_user(request):
    if 'user' in  request.GET and request.GET['user']:
        search_psn = request.GET.get("user")
        found_user = User.objects.filter(username=search_psn).first()
        print(found_user.id)
        posts = Post.objects.filter(user=found_user.id)

        context = {
            'user': found_user,
            'posts': posts,
        }
        
        return render(request, 'projects/spec_user.html', context)
    return redirect('welcome')

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            
            return redirect('login')
    else:
        form = SignUpForm()
       
    return render(request, 'users/register.html',{'form': form} )


@login_required
def profile(request):
    user = request.user
    posts = Post.objects.filter(user=user.id)
    if request.method == 'POST':
        up_form = UserUpdateForm(request.POST, instance=request.user)
        pr_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if up_form.is_valid() and pr_form.is_valid():
            up_form.save()
            pr_form.save()
            
            return redirect('profile')
    else:
        up_form = UserUpdateForm(instance=request.user)
        pr_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'user_form': up_form,
        'profile_form': pr_form,
        'posts': posts,
        
    }
    return render(request, 'users/profile.html', context)



class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer