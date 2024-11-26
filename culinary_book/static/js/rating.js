function rateRecipe(recipeId, rating) {
    fetch(`/api/rate-recipe/${recipeId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ rating: rating })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateRatingDisplay(recipeId, data.new_rating);
        }
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
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

function updateRatingDisplay(recipeId, newRating) {
    const ratingElement = document.querySelector(`#recipe-${recipeId} .rating`);
    ratingElement.textContent = newRating.toFixed(1);
}

