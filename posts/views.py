from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .forms import PostForm
from .models import Post

def post_create(request):
	form = PostForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		print form.cleaned_data.get("title")
		instance.save()


	# if request.method == "POST":
	# 	print request.POST.get("content")
	# 	title = request.POST.get("title")
	# 	Post.objects.create(title=title)
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
	queryset = Post.objects.all()
	if request.user.is_authenticated():
		context = {
			"object_list": queryset,
			"title": "List"
			}
	else:
		context = {
			"title": "List"
		}
	return render(request, "index.html", context)

def post_update(request):
	return HttpResponse("<h1>Update</h1>")

def post_delete(request):
	return HttpResponse("<h1>Delete</h1>")