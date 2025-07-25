from django.urls import path


from .views import RegisterView, GetTokenView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register panel"),
    path("get-token/", GetTokenView.as_view(), name="get token")
]
