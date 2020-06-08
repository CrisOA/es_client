from django.urls import include, path
from .views import BuildIndexNameSearch
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("search/", BuildIndexNameSearch.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
