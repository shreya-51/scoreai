/* script.js */

var wavesurfer = null;

// sets up the waveform player
function setupAudioPlayer() {
  wavesurfer = WaveSurfer.create({
    container: '#waveform',
    waveColor: '#EA4C89',
    progressColor: '#FFC0CB',
    //mediaControls: true
    backend: 'MediaElement'
  });

  wavesurfer.load(window.audioFileUrl);

  const playPauseButton = document.getElementById('playPauseButton');

  playPauseButton.addEventListener('click', () => {
    if (wavesurfer.isPlaying()) {
      wavesurfer.pause();
      playPauseButton.innerText = 'Play';
    } else {
      wavesurfer.play();
      playPauseButton.innerText = 'Pause';
    }
  });

}

function handleUserInputLLM() {

  const input = document.getElementById('user-input');

  input.addEventListener('keyup', (e) => {

    if (e.key === 'Enter') {

      const userValue = input.value;
      console.log('input: ', userValue)

      fetch('/ask_llm', { // Call 1 
           method: 'POST',
           body: JSON.stringify({userInput: userValue}),
           headers: {'Content-Type': 'application/json'}
         })
         .then(res => res.json()) 
         .then(askResult => {

           return fetch('/get-js-code', { // Call 2
             method: 'POST',
             body: JSON.stringify({result: askResult['result']}),
             headers: {'Content-Type': 'application/json'}
           });

         })
         .then(res => res.json())
         .then(jsCode => {
           console.log('code to be executed: ', jsCode['result'])
           eval(jsCode['result']); // Execute code
         });

    }

  });

}

// Initialize on page load
window.onload = function() {
  setupAudioPlayer();
  handleUserInputLLM();
};