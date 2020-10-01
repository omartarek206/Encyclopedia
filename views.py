from django.http import QueryDict, HttpResponse
from django.shortcuts import render
from django import forms

from . import util


def search_Check(query):
    match_List = []
    list_Entries = util.list_entries()
    for my_Entry in list_Entries:
        if my_Entry.startswith(query):
            match_List.append(my_Entry.casefold())
    return match_List


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })


def visit_Entry(request, my_Entry):
    if util.get_entry(my_Entry) is None:
        my_Entry = None
    return render(request, "encyclopedia/my_Entry.html", {
        "my_Entry": util.get_entry(my_Entry)
    })


def search(request):
    q = str(request.POST.get("q")).lower()
    return render(request, "encyclopedia/search.html", {
            "result": util.check_Entry(q)
        })

