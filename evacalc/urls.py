from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
	path('', views.index, name="index"),
	path('archive_date/', views.archive_date, name="archive_date"),  
	path('get_file/', views.get_file, name="get_file"),
	path('archive_grade', views.archive_grade, name="archive_grade")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
