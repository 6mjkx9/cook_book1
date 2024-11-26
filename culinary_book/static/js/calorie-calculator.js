function calculateCalories() {
  const ingredients = document.querySelectorAll('.ingredient');
  let totalCalories = 0;

  ingredients.forEach(ingredient => {
      const calories = parseInt(ingredient.dataset.calories);
      const quantity = parseInt(ingredient.querySelector('input').value);
      totalCalories += calories * quantity;
  });

  document.getElementById('total-calories').textContent = totalCalories;
}

