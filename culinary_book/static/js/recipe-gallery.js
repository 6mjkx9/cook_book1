document.addEventListener('DOMContentLoaded', function() {
  const gallery = document.querySelector('.recipe-gallery');
  const recipes = gallery.querySelectorAll('.recipe-card');

  recipes.forEach(recipe => {
      recipe.addEventListener('click', function() {
          this.classList.toggle('expanded');
      });
  });
});

