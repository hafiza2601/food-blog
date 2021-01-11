from django.urls import path
from . import views
from django.conf.urls.static import static
from django.views.static import serve
from django.conf.urls import url


urlpatterns = [
    path('home',views.home, name='home'),
    path('blog',views.blog,name='bolg'),
    path('about_us',views.about_us, name = 'about_us'),
    path('contact',views.contact, name = 'contact'),
    path('signup',views.handlesignup, name='signup'),
    path('login',views.handlelogin, name='login'),
    path('logout',views.handlelogout, name='logout'),
    path('blog/postcomment',views.postComment,name='blogcomment'),
    path('search',views.search, name='search'),
    #detail blog post
    path('blog/<str:slug>/', views.post_detail, name='post_detail'),
    #path('post/new/', views.post_new, name='post_new'),
    #path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    #path('About_us')
    url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
    
]
