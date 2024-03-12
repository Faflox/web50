from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from .util import get_entry
import markdown
import random

from . import util

def convert_to_html(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

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
    titles = util.list_entries()
    title = random.choice(titles)
    return redirect("entry", title=title)

def edit_page(request, title):
    if request.method == "POST":
        content = request.POST["content"]
        util.save_entry(title, content)
        return redirect("entry", title=title)
    else:
        content = get_entry(title)
        return render(request, "encyclopedia/edit_page.html", {"title": title, "content": content})
    
def search(request):
    if request.method == "POST":
        query =  request.POST["q"]
        content = convert_to_html(query)
        if content is not None:
            return redirect(request, "encyclopedia/entry.html", {
                "title": query, 
                "content": content
                })
        else:
            results = []
            for entry in util.list_entries():
                if query.lower() in entry.lower():
                    results.append(entry)
            return render(request, "encyclopedia/search.html", {
                "results": results
                })   