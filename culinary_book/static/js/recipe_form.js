document.addEventListener('DOMContentLoaded', function() {
  const form = document.querySelector('form');
  const submitButton = form.querySelector('button[type="submit"]');

  form.addEventListener('submit', function(e) {
      e.preventDefault();
      submitButton.disabled = true;
      submitButton.textContent = 'Додавання...';
      this.submit();
  });
});
