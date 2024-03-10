from django.http import Http404
from django.shortcuts import render, redirect
from .util import get_entry
import markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_page(request, title):
    content = get_entry(title)
    if content is not None:
        html_content = markdown.markdown(content)
        return render(request, "encyclopedia/entry.html", {"title": title, "content": html_content})
    else:
        raise Http404("Entry does not exist")
    
    
def new_page(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        if title in util.list_entries():
            return render(request, "encyclopedia/new_page.html", {"error": "Entry already exists"})
        elif not content or not title:
            return render(request, "encyclopedia/new_page.html", {"error": "Content cannot be empty"})
        else:
            util.save_entry(title, content)
            return redirect("entry", title=title)
    else:
        return render(request, "encyclopedia/new_page.html")
    
def random_page(request):
    title = util.random_page()
    return redirect("entry", title=title)