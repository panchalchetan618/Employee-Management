from django.urls import path
from .views import FileView, PersonView, index
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"persons", PersonView, basename="person")

urlpatterns = [
    path("upload/", FileView.as_view(), name="fileView"),
    path("", index, name="index"),
] + router.urls
