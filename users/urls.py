from django.urls import path
from .views import RegisterView, LoginView, UserView, LogoutView, EditUserRoleView, ExitSiteView, GetUserListView, GetUserInfoByName

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('editRole', EditUserRoleView.as_view()),
    path('exist', ExitSiteView.as_view()),
    path('userlist', GetUserListView.as_view()),
    path('info', GetUserInfoByName.as_view())
]

