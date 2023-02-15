from django.urls import path

from djsniper.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    UserPersonalCreateView,
    UserEnterpriseCreateView,
    OrderCreateView,
    UserProfileView,
    user_password_view,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>", view=user_detail_view, name="detail"),
    path("profile/<str:username>", view=UserProfileView, name="profile"),
    path("personal/", view=UserPersonalCreateView.as_view, name="personal"),
    path("enterprise/", view=UserEnterpriseCreateView.as_view(), name="enterprise"),
    path("password/<str:username>", view=user_password_view, name="password")
]
