var deferredInstallPrompt;
var installButton = document.getElementById('button-install');
if (installButton !== null) {
  if (window.matchMedia('(display-mode: standalone)').matches) {
    installButton.style.display = 'none';
  } else {
    installButton.addEventListener('click', installPWA);
  }
}

window.addEventListener('beforeinstallprompt', saveBeforeInstallPromptEvent);

function saveBeforeInstallPromptEvent(evt) {
  evt.preventDefault();
  deferredInstallPrompt = evt;
  if (installButton !== null) {
    installButton.removeAttribute('hidden');
  }
}

function installPWA(e) {
  deferredInstallPrompt.prompt();
  if (installButton !== null) {
    installButton.setAttribute('hidden', true);
  }
  deferredInstallPrompt.userChoice
  .then((choice) => {
    if (choice.outcome === 'accepted') {
      console.log('User accepted the prompt', choice);
    } else {
      console.log('User dismissed the prompt', choice);
    }
    deferredInstallPrompt = null;
  });
}

window.addEventListener('appinstalled', logAppInstalled);

function logAppInstalled(e) {
  console.log('App was installed.', e);
}
