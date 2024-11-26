from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})
    
class Recipe(models.Model):
    title = models.CharField(max_length=500)
    slug = models.SlugField(unique=True, blank=True) 
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='recipes', default=1)
    description = models.TextField(blank=True)
    ingredients = models.TextField()
    instructions = models.TextField()
    content = models.TextField()
    cooking_time = models.PositiveIntegerField(help_text="Час приготування в хвилинах")
    servings = models.PositiveIntegerField()
    image = models.ImageField(upload_to='recipe_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(null=True, blank=True, default=0)

    def save(self, *args, **kwargs):
        if not self.slug:  
            self.slug = slugify(self.title)
        while Recipe.objects.filter(slug=self.slug).exists():
            self.slug = f"{slugify(self.title)}-{Recipe.objects.count() + 1}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipes:recipe_detail', kwargs={'slug': self.slug})

class Review(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Оновлення середнього рейтингу рецепта
        avg_rating = self.recipe.reviews.aggregate(models.Avg('rating'))['rating__avg']
        self.recipe.rating = avg_rating or 0
        self.recipe.save()

    def __str__(self):
        return f"Відгук на {self.recipe.title} від {self.user.username}"
class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_categories = models.ManyToManyField(Category)
    dietary_restrictions = models.TextField(blank=True)

class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

class ShoppingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredients = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Список покупок для {self.recipe.title} користувача {self.user.username}"



class SocialShare(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    platform = models.CharField(max_length=50)
    shared_at = models.DateTimeField(auto_now_add=True)

