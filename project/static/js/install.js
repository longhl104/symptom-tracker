let deferredInstallPrompt = null;
const installButton = document.getElementById('button-install');
console.log('install', installButton)
if (installButton !== null) {
  installButton.addEventListener('click', installPWA);
}

window.addEventListener('beforeinstallprompt', saveBeforeInstallPromptEvent);

function saveBeforeInstallPromptEvent(evt) {
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
