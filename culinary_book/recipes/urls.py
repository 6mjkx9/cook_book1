from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('recipe/new/', views.RecipeCreateView.as_view(), name='recipe_create'),
    path('recipe/<slug:slug>/', views.RecipeDetailView.as_view(), name='recipe_detail'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('search/', views.search_recipes, name='search_recipes'),
    path('recipe/<int:recipe_id>/review/', views.add_review, name='add_review'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('preferences/', views.user_preferences, name='user_preferences'),
    path('recommend/', views.recommend_recipes, name='recommend_recipes'),
    path('share/<int:recipe_id>/', views.share_recipe, name='share_recipe'),
    path('shopping-list/', views.shopping_list, name='shopping_list'),
    path('recommended_recipes/', views.RecommendedRecipesView.as_view(), name='recommended_recipes'),
    path('remove-from-shopping-list/<int:shopping_list_id>/', views.remove_from_shopping_list, name='remove_from_shopping_list'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]

