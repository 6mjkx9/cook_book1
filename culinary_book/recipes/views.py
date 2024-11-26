from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.db.models import Avg
from .models import Recipe, Category, Review, UserPreference, Recommendation, ShoppingList, SocialShare
from .forms import RecipeForm, ReviewForm, CustomUserCreationForm, CustomAuthenticationForm
from django.db.models import Avg, Q
from django.contrib import messages

class HomeView(ListView):
    model = Recipe
    template_name = 'home.html'
    context_object_name = 'recipes'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recommended_recipes'] = Recipe.objects.order_by('-rating')[:3]
        return context

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recommended_recipes'] = Recipe.objects.order_by('-rating')[:3]
        return context


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipe_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        messages.success(self.request, 'Рецепт успішно додано!')
        return redirect('home')
    
    def get_success_url(self):
        return reverse_lazy('recipe_detail', kwargs={'pk': self.object.pk})

class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipe_form.html'
    success_url = reverse_lazy('home')

class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipe
    template_name = 'recipe_confirm_delete.html'
    success_url = reverse_lazy('home')

class ShoppingListView(LoginRequiredMixin, ListView):
    template_name = 'recipes/shopping_list.html'
    context_object_name = 'shopping_lists'

    def get_queryset(self):
        return ShoppingList.objects.filter(user=self.request.user)
    
class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipes'] = Recipe.objects.filter(category=self.object)
        return context


class SearchView(ListView):
    model = Recipe
    template_name = 'search_results.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Recipe.objects.filter(title__icontains=query)
    
def search_recipes(request):
    query = request.GET.get('q')
    results = Recipe.objects.filter(
        Q(title__icontains=query) |
        Q(ingredients__icontains=query) |
        Q(instructions__icontains=query)
    ).distinct() if query else Recipe.objects.none()
    return render(request, 'search_results.html', {'results': results, 'query': query})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})
@login_required
def add_review(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.recipe = recipe
            review.user = request.user
            review.save()
            messages.success(request, 'Ваш відгук додано успішно!')
            return redirect('recipe_detail', pk=recipe.pk)
    return redirect('recipe_detail', pk=recipe.pk)

@login_required
def user_preferences(request):
    preference, created = UserPreference.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        categories = request.POST.getlist('categories')
        dietary_restrictions = request.POST.get('dietary_restrictions', '')
        preference.favorite_categories.set(categories)
        preference.dietary_restrictions = dietary_restrictions
        preference.save()
        return redirect('home')
    categories = Category.objects.all()
    return render(request, 'recipes/user_preferences.html', {'preference': preference, 'categories': categories})

@login_required
def recommend_recipes(request):
    preference = UserPreference.objects.get(user=request.user)
    favorite_categories = preference.favorite_categories.all()
    recommended_recipes = Recipe.objects.filter(category__in=favorite_categories).order_by('?')[:5]
    return render(request, 'recipes/recommended_recipes.html', {'recipes': recommended_recipes})

@login_required
def share_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.method == 'POST':
        platform = request.POST.get('platform')
        SocialShare.objects.create(user=request.user, recipe=recipe, platform=platform)
        return redirect('recipe_detail', slug=recipe.slug)
    return render(request, 'recipes/share_recipe.html', {'recipe': recipe})

@login_required
def shopping_list(request):
    shopping_lists = ShoppingList.objects.filter(user=request.user)
    return render(request, 'recipes/shopping_list.html', {'shopping_lists': shopping_lists})


class RecommendedRecipesView(ListView):
    model = Recipe
    template_name = 'recipes/recommended_recipes.html'
    context_object_name = 'recommended_recipes'

    def get_queryset(self):
        return Recipe.objects.order_by('-rating')[:10]


@login_required
def remove_from_shopping_list(request, shopping_list_id):
    shopping_list = get_object_or_404(ShoppingList, id=shopping_list_id, user=request.user)
    recipe_title = shopping_list.recipe.title
    shopping_list.delete()
    messages.success(request, f"Інгредієнти для {recipe_title} видалено зі списку покупок.")
    return redirect('shopping_list')

@login_required
def voice_instructions(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'recipes/voice_instructions.html', {'recipe': recipe})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

queryset = Recipe.objects.all().order_by('created_at')
