from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms

from . import util


class MyForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content")


def search_Check(query):
    match_List = []
    list_Entries = util.list_entries()
    for my_Entry in list_Entries:
        if my_Entry.startswith(query):
            match_List.append(my_Entry.casefold())
    return match_List


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def visit_Entry(request, my_Entry):
    if util.get_entry(my_Entry) is None:
        my_Entry = None
    return render(request, "encyclopedia/my_Entry.html", {
        "my_Entry": util.get_entry(my_Entry)
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
