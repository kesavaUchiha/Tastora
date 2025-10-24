from django.urls import path
from . import views
app_name='recipe_management'

urlpatterns=[
    path('add/',views.AddRecipe.as_view(),name='add')
]
