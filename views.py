from django.http import QueryDict
from django.shortcuts import render
from django import forms

from . import util

'''
def search_Check(list_Entries,result):
    match_List =[]
    for my_Entry in list_Entries:
        if my_Entry.startswith(result):
            match_List.append(my_Entry)
    return match_List
'''





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
    return render(request, "encyclopedia/search.html", {
        "result": request.POST
    })
