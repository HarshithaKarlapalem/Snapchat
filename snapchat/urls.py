from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('home',views.home,name="home"),
    path('User', views.home, name="home"),
    path('user', views.user, name="home"),
    path('homeredirect', views.homeredirect, name='redirect'),
    path('signup', views.signUp, name="signup"),    
    path('signin', views.signIn, name="signin"),
    path('LoginIn',views.user,name="signin"),
    path('SignUp',views.signIn,name="signup"),
]
