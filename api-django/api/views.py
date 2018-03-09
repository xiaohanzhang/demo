from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

print('init api.views')

# Create your views here.
def index(request):
    return HttpResponse('hello')

class MyView(View):

    @classmethod
    def as_view(cls, **kwargs):
        print('init MyView.as_view')
        return super(MyView, cls).as_view(**kwargs)

    def __init__(self, *args, **kwargs):
        print('init MyView')
        super(MyView, self)

    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, View!')



