from atexit import register
from django import template
from .. import models

register = template.Library()


@register.inclusion_tag('books/include/comments.html', takes_context=True)
def get_comments(context):
    comments = models.Comment.objects.filter(book=context['book'], moderation=False)
    return {'comments': comments}
