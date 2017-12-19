from django.conf.urls import url
from app import views
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^login/$',views.loginuser, name ="login"),
	url(r'^logout/$',views.logoutuser, name ="login"),
	url(r'^download/$', views.download , name = 'download'),
	url(r'^upload/', views.upload , name = 'upload'),
	url(r'^add/', views.add , name = 'add'),
	url(r'^update/', views.updatetotal , name = 'upload'),
]
