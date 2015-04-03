from django import template

# adapted from http://stackoverflow.com/a/1881894
register = template.Library()

@register.inclusion_tag('post_template.html', takes_context=True)
def render_post(context):
	list_of_posts = context['list_of_posts']
	user = context['user']
	context_for_rendering_inclusion_tag = {'list_of_posts': list_of_posts, 'user': user}
	return context_for_rendering_inclusion_tag