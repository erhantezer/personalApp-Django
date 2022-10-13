
from django.urls import include, path
from .views import DepartmentPersonalView, DepartmentView, PersonalGetUpdateDelete, PersonalListCreate

urlpatterns = [
    path('', DepartmentView.as_view()),
    path('department/<str:department>/', DepartmentPersonalView.as_view()),
    path("personal/", PersonalListCreate.as_view()),
    path("personal/<int:pk>/", PersonalGetUpdateDelete.as_view()),
]
