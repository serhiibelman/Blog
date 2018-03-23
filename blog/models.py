from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save

from django.utils.text import slugify

class Category(models.Model):
	"""
	Category model
	"""
	category_name = models.CharField(max_length=30, unique=True)
	slug = models.SlugField(unique=True)

	def __str__(self):
		return self.category_name

class Article(models.Model):
	"""
	Article model
	"""
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	category = models.ManyToManyField(Category)
	article_title = models.CharField(max_length=250)
	article_content = models.TextField()
	comments_number = models.IntegerField(default=0)
	slug = models.SlugField(unique=True)
	pub_date = models.DateTimeField('date published')

	def __str__(self):
		return self.article_title

class Comment(models.Model):
	"""
	Comment model
	"""
	article = models.ForeignKey(Article, on_delete=models.CASCADE)
	comment_text = models.TextField()
	user_name = models.CharField(max_length=50, default='')
	user_email = models.EmailField(max_length=100)

	def __str__(self):
		return self.user_name + ': ' + self.comment_text

class HashTag(models.Model):
	""" 
	HashTag model 
	"""
	name = models.CharField(max_length=200, unique=True)
	article = models.ManyToManyField(Article)

	def __str__(self):
		return self.name


def create_slug(instance, new_slug=None):
	slug = slugify(instance.article_title)
	if new_slug is not None:
		slug = new_slug
	qs = Article.objects.filter(slug=slug).order_by('-id')
	exists = qs.exists()
	if exists:
		new_slug = '%s-%s' % (slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug

def pre_save_article_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)


pre_save.connect(pre_save_article_receiver, sender=Article)