"""
URL configuration for Travel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from trvlblgapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('feedback/', views.view_feedback, name='feedback'),
    path('gallery',views.gallery),
    path('post_details/<int:post_id>/', views.single_view, name='single_view'),

    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout',views.logout),

    path('user_home/', views.user_home, name='user_home'),

    path('profile',views.user_profile),
    path('profile_update/<int:id>',views.pro_edit),
    path('profile_updadte/<int:id>',views.update_profile),

    path('create_post', views.create, name='create_post'),
    path('api/create_post', views.create_post_api, name='create_post_api'),
    path('view_post',views.view),
    path('api/delete_post/<int:post_id>/', views.delete_post_api, name='delete_post_api'),
    path('update_post/<int:post_id>/', views.update_post, name='update_post'),
    path('api/update_post/<int:post_id>/', views.update_post_api, name='update_post_api'),


    path('user_feedback',views.user_feedback),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
