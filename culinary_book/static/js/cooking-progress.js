function updateCookingProgress(step) {
  const progressBar = document.querySelector('.cooking-progress');
  const totalSteps = progressBar.dataset.totalSteps;
  const progress = (step / totalSteps) * 100;
  
  progressBar.style.width = `${progress}%`;
  progressBar.textContent = `${Math.round(progress)}%`;
}

