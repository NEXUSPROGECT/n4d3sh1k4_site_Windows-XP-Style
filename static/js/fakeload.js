let value = 0;
const progress = document.getElementById('progress');

const fakeLoading = setInterval(() => {
  if (value < 90) {
    value += Math.random() * 5;
    progress.value = value;
  }
}, 200);

window.addEventListener('load', () => {
  clearInterval(fakeLoading);

  const finish = setInterval(() => {
    if (value < 100) {
      value += 2;
      progress.value = value;
    } else {
      clearInterval(finish);
      document.getElementById('loader').style.display = 'none';
      document.body.classList.add('loaded');
      openWindow('projectsWindow');
      openWindow('profileWindow');
      openWindow('aboutWindow');
    }
  }, 30);
});
