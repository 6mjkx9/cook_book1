from django.core.management.base import BaseCommand
from recipes.models import Category
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Add predefined categories'

    def handle(self, *args, **kwargs):
        categories = [
            'Салати','Супи', 'Основні страви', 'Десерти', 
            'Напої без алкогольні', 'Напої алкогольні', 
            'Закуски', 'Випічка', 'Вегетаріанські страви', 
            'Страви з мяса', 'Страви з риби'
        ]

        for category_name in categories:
            base_slug = slugify(category_name)
            slug = base_slug
            counter = 1
            
            # Ensure slug is unique
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            # Create or retrieve the category
            category, created = Category.objects.get_or_create(
                name=category_name,
                defaults={'slug': slug}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Category "{category_name}" created with slug "{slug}".'))
            else:
                self.stdout.write(f'Category "{category_name}" already exists.')
