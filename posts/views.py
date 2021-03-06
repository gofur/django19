from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from .forms import PostForm
from .models import Post

def post_create(request):
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		# message success
		messages.success(request, "Successfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())
	else:
		messages.error(request, "Failed Created")

	context = {
		"form": form,
	}
	return render(request, "post_form.html", context)

def post_detail(request, id_detail=None): #retrieve
	# instance = Post.objects.get(id=1)
	instance = get_object_or_404(Post,id=id_detail)
	context = {
		"title": instance.title,
		"instance": instance,
	}
	return render(request, "post_detail.html", context)

def post_list(request):
	queryset_list = Post.objects.all() #.order_by("-timestamp")
	paginator = Paginator(queryset_list, 25) # Show 25 contacts per page

	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
	# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
	# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)


	if request.user.is_authenticated():
		context = {
			"object_list": queryset,
			"title": "List"
		}
	else:
		context = {
			"title": "List"
		}
	return render(request, "post_list.html", context)


def post_update(request, id_detail=None):
	instance = get_object_or_404(Post,id=id_detail)
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		# message success
		messages.success(request, "<a href='#'>Item</a> Updated", extra_tags='html_safe')
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"title": instance.title,
		"instance": instance,
		"form":form,
	}

	return render(request, "post_form.html", context)

def post_delete(request, id_detail=None):
	instance = get_object_or_404(Post,id=id_detail)
	instance.delete()
	messages.success(request, "Successfully Deleted")
	return redirect("posts:list")
