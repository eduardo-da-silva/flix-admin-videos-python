from django.urls import path
from django_app import container
from .api import CategoryResource

urlpatterns = [
    path('categories/', CategoryResource.as_view(
        create_use_case=container.use_case_category_create_category,
        list_use_case=container.use_case_category_list_categories
    ))
]
