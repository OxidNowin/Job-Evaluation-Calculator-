from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
	#path('', views.index, name="index"),
	path('archive_date/', views.archive_date, name="archive_date"),  
	path('returnexcel/', views.returnexcel, name="returnexcel"),
	path('archive_grade', views.archive_grade, name="archive_grade"),
	path('', views.skills_section, name="skills_section"),
	#path('problems_section/', views.problems_section, name="problems_section"),
	#path('responsibility_section/', views.responsibility_section, name="responsibility_section"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
