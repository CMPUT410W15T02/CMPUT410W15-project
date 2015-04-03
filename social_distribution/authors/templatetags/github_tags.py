from django import template

# adapted from http://stackoverflow.com/a/1881894
register = template.Library()

@register.inclusion_tag('github_template.html', takes_context=True)
def render_github(context):
	user = context['user']
	my_profile = context['my_profile']
	list_of_github = context['list_of_github']

	context_for_rendering_inclusion_tag = {'list_of_github': list_of_github, 'my_profile': my_profile}
	return context_for_rendering_inclusion_tag