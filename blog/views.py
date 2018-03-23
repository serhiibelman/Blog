from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Article, Comment, Category, HashTag
from .forms import CommentForm, AddArticleForm, AddCategoryForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

def index(request):
	"""
	Main page
	"""
	articles = Article.objects.order_by('-pub_date')[:5]
	categories = Category.objects.all()
	return render(request, 'blog/index.html', {'articles': articles, 'categories': categories})

def detail(request, article_id, slug):
	"""
	Show post and comments
	"""
	username = request.user.get_username()
	if username:
		email = request.user.email
	if not username:
		username = 'AnonymousUser'
		email = 'foo@example.com'
	form = CommentForm(initial={'user_name': username, 'user_email': email}, auto_id=False)
	article = get_object_or_404(Article, id=article_id)
	comments = Comment.objects.filter(article_id=article_id)
	return render(request, 'blog/detail.html', {'article': article, 'comments': comments, 'form': form})

def selected_category(request, slug):
	"""
	Show all posts in some category
	"""
	category = get_object_or_404(Category, slug=slug)
	articles = Article.objects.filter(category__slug=slug)
	return render(request, 'blog/selected_category.html', {'articles': articles, 'slug': slug})

def add_comment(request, article_id, slug):
	article = get_object_or_404(Article, id=article_id)
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		form = CommentForm(request.POST or None)
		# check whether it's valid:
		if form.is_valid():
			# Create, but don't save the new comment instance.
			comment = form.save(commit=False)
			comment.article = article
			# Update the comment
			comment.comment_text = form.cleaned_data['comment_text']
			username = request.user.get_username()
			comment.user_name = form.cleaned_data['user_name']
			comment.user_email = form.cleaned_data['user_email']
			article.comments_number = article.comment_set.count() + 1
			# Save the new instance.
			article.save()
			comment.save()
	return HttpResponseRedirect(reverse('blog:detail', args=(article_id, article.slug)))

@login_required(login_url='loginsys:login_user')
def admin_panel(request):
	return render(request, 'blog/admin_panel.html')

# Article
@login_required(login_url='loginsys:login_user')
def add_article(request):
	# if a GET (or any other method) we'll create a blank form
	form = AddArticleForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			article = form.save(commit=False)
			username = request.user.get_username()
			categories = form.cleaned_data['category']
			article_content = form.cleaned_data['article_content']
			article.author = User.objects.get(username=username)
			article.article_title = form.cleaned_data['article_title']
			article.article_content = article_content
			article.pub_date = timezone.now()
			article.save()
			# add word to hashtag if word start with '#'
			words = form.cleaned_data['article_content'].split(' ')
			for word in words:
				if word.startswith('#'):
					hash_tag, created = HashTag.objects.get_or_create(name=word)
					hash_tag.article.add(article)

			for category in categories:
				article.category.add(category)
		return HttpResponseRedirect(reverse('blog:admin_panel'))
	return render(request, 'blog/add_article.html', {'form': form})

@login_required(login_url='loginsys:login_user')
def article_for_change(request):
	articles = Article.objects.all()
	return render(request, 'blog/article_for_change.html', {'articles': articles})

@login_required(login_url='loginsys:login_user')
def change_article(request, article_id):
	article = get_object_or_404(Article, id=article_id)
	if request.method == 'POST':
		article.article_title = request.POST['article_title']
		article.article_content = request.POST['article_content']
		article.slug = request.POST['slug']
		article.save()
		return HttpResponseRedirect(reverse('blog:admin_panel'))
	return render(request, 'blog/change_article.html', {'article': article})

@login_required(login_url='loginsys:login_user')
def del_article(request):
	if request.method == 'POST':
		article_id = request.POST['article']
		article = get_object_or_404(Article, id=article_id)
		article.delete()
		return HttpResponseRedirect(reverse('blog:del_article'))
	articles = Article.objects.all()
	return render(request, 'blog/del_article.html', {'articles': articles})

# Category
@login_required(login_url='loginsys:login_user')
def add_category(request):
	form = AddCategoryForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			category = form.save(commit=False)
			category.category_name = form.cleaned_data['category_name']
			category.slug = form.cleaned_data['slug']
			category.save()
		return HttpResponseRedirect(reverse('blog:admin_panel'))
	return render(request, 'blog/add_category.html', {'form': form})

@login_required(login_url='loginsys:login_user')
def category_for_change(request):
	categories = Category.objects.all()
	return render(request, 'blog/category_for_change.html', {'categories': categories})

@login_required(login_url='loginsys:login_user')
def change_category(request, category_id):
	category = get_object_or_404(Category, id=category_id)
	if request.method == 'POST':
		category.category_name = request.POST['category_name']
		category.slug = request.POST['slug']
		category.save()
		return HttpResponseRedirect(reverse('blog:admin_panel'))
	return render(request, 'blog/change_category.html', {'category': category})

@login_required(login_url='loginsys:login_user')
def del_category(request):
	if request.method == 'POST':
		category_id = request.POST['category']
		category = get_object_or_404(Category, id=category_id)
		category.delete()
		return HttpResponseRedirect(reverse('blog:del_category'))
	categories = Category.objects.all()
	return render(request, 'blog/del_category.html', {'categories': categories})

# Change password
@login_required(login_url='loginsys:login_user')
def change_password(request):
	user = get_object_or_404(User, username=request.user)
	form = PasswordChangeForm(request.user, request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)
			messages.success(request, 'Your password was successfully updated!')
			return HttpResponseRedirect(reverse('blog:admin_panel'))
		else:
			messages.error(request, 'Please correct the error below.')			
	return render(request, 'blog/change_password.html', {'form': form})

# Comment
@login_required(login_url='loginsys:login_user')
def del_comment(request):
	form = AddCategoryForm(request.POST or None)
	if request.method == 'POST':
		comment_id = request.POST['comment']
		comment = get_object_or_404(Comment, id=comment_id)
		article = Article.objects.get(comment__id=comment_id)
		comment.delete()
		
		article.comments_number = article.comment_set.count()
		article.save()
		return HttpResponseRedirect(reverse('blog:del_comment'))
	comments = Comment.objects.all()
	return render(request, 'blog/del_comment.html', {'comments': comments})

@login_required(login_url='loginsys:login_user')
def comment_for_change(request):
	comments = Comment.objects.all()
	return render(request, 'blog/comment_for_change.html', {'comments': comments})

@login_required(login_url='loginsys:login_user')
def change_comment(request, comment_id):
	comment = get_object_or_404(Comment, id=comment_id)
	if request.method == 'POST':
		comment.comment_text = request.POST['comment_text']
		comment.user_name = request.POST['user_name']
		comment.user_email = request.POST['user_email']
		comment.save()
		return HttpResponseRedirect(reverse('blog:admin_panel'))
	return render(request, 'blog/change_comment.html', {'comment': comment})