from django import template

# adapted from http://stackoverflow.com/a/1881894
register = template.Library()

@register.inclusion_tag('post_template.html', takes_context=True)
def render_post(context):
	post = context['post']
	user = context['user']
	context_for_rendering_inclusion_tag = {'post': post, 'user': user}
	return context_for_rendering_inclusion_tag