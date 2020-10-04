from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms

from . import util, markdown2


class MyForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content")


class form(MyForm):
    title = None


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def visit_Entry(request, my_Entry):
    if util.get_entry(my_Entry) is None:
        return render(request, "encyclopedia/badentry.html")
    return render(request, "encyclopedia/my_Entry.html", {
        "title": my_Entry,
        "content": markdown2.markdown(util.get_entry(my_Entry))
    })


def edit(request, title):
    if request.method == 'POST':
        myform = form(request.POST)
        if myform.is_valid():
            content = myform.cleaned_data["content"]
            util.save_entry(title, content)
            return visit_Entry(request, title)
        else:
            return render(request, "encyclopedia/new.html", {
                "myform": myform
            })
    else:
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })


def search(request):
    if request.method == 'POST':
        q = str(request.POST.get("q")).lower()
        if util.get_entry(q) is not None:
            return HttpResponseRedirect(f"{q}")
        return render(request, "encyclopedia/search.html", {
            "result": util.check_Entry(q)
        })
    else:
        return render(request, "encyclopedia/index.html")


def new(request):
    if request.method == 'POST':
        myform = MyForm(request.POST)
        if myform.is_valid():
            title = myform.cleaned_data["title"]
            if util.get_entry(title) is not None:
                return render(request, "encyclopedia/badnew.html")
            content = myform.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(f"{title}")
        else:
            return render(request, "encyclopedia/new.html", {
                "myform": myform
            })
    return render(request, "encyclopedia/new.html", {
        "myform": MyForm
    })


def random(request):
    title = util.random_Entry()
    return visit_Entry(request, title)
