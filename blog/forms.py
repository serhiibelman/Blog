from django.forms import Textarea, ModelForm, ModelMultipleChoiceField, EmailField, CharField
from .models import Article, Comment, Category


class CommentForm(ModelForm):
	class Meta:
		model = Comment
		fields = ['user_name', 'user_email', 'comment_text']
		widgets = {
            'comment_text': Textarea(attrs={'cols': 80, 'rows': 5}),
        }

class AddArticleForm(ModelForm):
	category = ModelMultipleChoiceField(queryset=Category.objects.all())
	class Meta:
		model = Article
		fields = ['article_title', 'article_content', 'category']
		article_content = {
            'comment_text': Textarea(attrs={'cols': 80, 'rows': 5}),
        }

class AddCategoryForm(ModelForm):
	class Meta:
		model = Category
		fields = ['category_name', 'slug']
