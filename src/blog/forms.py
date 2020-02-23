from django import forms

from .models import BlogPost, BlogPostComment


class BlogPostForm(forms.ModelForm):
	class Meta:
		model=BlogPost
		fields = [
			'title',
			'slug',
			'content'
			]
			
class BlogPostCommentForm(forms.ModelForm):
	class Meta:
		model=BlogPostComment
		fields = [
			'author',
			'content'
			]
		