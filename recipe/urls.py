from django.urls import path
from . import views
app_name='recipe'
urlpatterns=[
    path('home/',views.HomePage.as_view(),name='home'),
    path('recipe//',views.RecipePage.as_view(),name='recipe')
]