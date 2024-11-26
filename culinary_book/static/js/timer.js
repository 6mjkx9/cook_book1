function createTimer(duration) {
  let timer = duration, minutes, seconds;
  const timerDisplay = document.getElementById('timer');
  const intervalId = setInterval(function () {
      minutes = parseInt(timer / 60, 10);
      seconds = parseInt(timer % 60, 10);

      minutes = minutes < 10 ? "0" + minutes : minutes;
      seconds = seconds < 10 ? "0" + seconds : seconds;

      timerDisplay.textContent = minutes + ":" + seconds;

      if (--timer < 0) {
          clearInterval(intervalId);
          timerDisplay.textContent = "Час вийшов!";
      }
  }, 1000);
}

