document.addEventListener('DOMContentLoaded', (event) => {
  // Favorite button functionality
  document.querySelectorAll('.favorite-btn').forEach(button => {
      button.addEventListener('click', function() {
          const recipeId = this.dataset.recipeId;
          fetch(`/toggle_favorite/${recipeId}/`, {
              method: 'POST',
              headers: {
                  'X-CSRFToken': getCookie('csrftoken'),
              },
          })
          .then(response => response.json())
          .then(data => {
              if (data.status === 'success') {
                  this.textContent = this.textContent.includes('Add') ? 'Remove from favorites' : 'Add to favorites';
              }
          });
      });
  });

  // Filter functionality
  document.querySelectorAll('.filter-btn').forEach(button => {
      button.addEventListener('click', function() {
          const filter = this.dataset.filter;
          // Implement filter logic here
          console.log(`Filter by ${filter}`);
      });
  });

  // Share functionality
  document.querySelectorAll('.share-btn').forEach(button => {
      button.addEventListener('click', function() {
          const platform = this.dataset.platform;
          const url = encodeURIComponent(window.location.href);
          const text = encodeURIComponent('Check out this amazing recipe!');
          let shareUrl;

          if (platform === 'facebook') {
              shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${url}`;
          } else if (platform === 'twitter') {
              shareUrl = `https://twitter.com/intent/tweet?url=${url}&text=${text}`;
          }

          window.open(shareUrl, '_blank');
      });
  });

  // Helper function to get CSRF token
  function getCookie(name) {
      let cookieValue = null;
      if (
document.cookie && document.cookie !== '') {
          const cookies = document.cookie.split(';');
          for (let i = 0; i < cookies.length; i++) {
              const cookie = cookies[i].trim();
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }
});

