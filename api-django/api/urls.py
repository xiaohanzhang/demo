from django.urls import path

from api.views import MyView, index

urlpatterns = [
    path('', index, name='index'),
    path('view', MyView.as_view()),
]