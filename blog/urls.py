from django.urls import path, include
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:article_id>/<slug>/', views.detail, name='detail'),
    path('detail/<int:article_id>/<slug>/add_comment/', views.add_comment, name='add_comment'),
    path('category/<slug>/', views.selected_category, name='selected_category'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    # Article
    path('admin_panel/add_article/', views.add_article, name='add_article'),
    path('admin_panel/article/', views.article_for_change, name='article_for_change'),
    path('admin_panel/change_article/<int:article_id>/', views.change_article, name='change_article'),
    path('admin_panel/del_article/', views.del_article, name='del_article'),
    # Category
    path('admin_panel/add_category/', views.add_category, name='add_category'),
    path('admin_panel/category/', views.category_for_change, name='category_for_change'),
    path('admin_panel/change_category/<int:category_id>/', views.change_category, name='change_category'),
    path('admin_panel/del_category/', views.del_category, name='del_category'),
    # Comment
    path('admin_panel/del_comment/', views.del_comment, name='del_comment'),
    path('admin_panel/comment/', views.comment_for_change, name='comment_for_change'),
    path('admin_panel/comment/<int:comment_id>/', views.change_comment, name='change_comment'),
    # Change password
    path('admin_panel/change_password/', views.change_password, name='change_password'),
]
