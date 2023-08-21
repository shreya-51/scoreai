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

function showSnackbar(message) {
  var x = document.getElementById("snackbar");
  x.textContent = message;
  x.className = "show";
  setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
}

function test_audio_editing_code() {
  // Add reverb 
  var reverb = new Pizzicato.Effects.Reverb({
    time: 1.5,
    decay: 3,
    reverse: true,
    mix: 0.5
  });

  wavesurfer.play();
  wavesurfer.addEffect(reverb);
}


function handleUserInputLLM() {

  const input = document.getElementById('user-input');

  input.addEventListener('keyup', (e) => {

    if (e.key === 'Enter') {

      const userValue = input.value;
      console.log('input: ', userValue)

      var query = "You are a sound engineer that is editing a track provided loaded into an already-created wavesurfer.js element. There are 2 categories of requests from the user: 1. Command can be executed using wavesurfer.js library only. 2. Command is to add an effect to the audio. IMPORTANT: **Return only the number of the category.** Which category is the following command in? Command: "
      var final_query = query + userValue


      fetch('/ask_llm_only', { // Call 1 
        method: 'POST',
        body: JSON.stringify({userInput: final_query, error: false, errorValue: 'nothing'}),
        headers: {'Content-Type': 'application/json'}
      })
      .then(res => res.json())
      .then(askResult => {
        console.log("category: ", askResult['result'])
      })
      

      fetch('/ask_llm', { // Call 1 
           method: 'POST',
           body: JSON.stringify({userInput: userValue, error: false, errorValue: 'nothing'}),
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
           showSnackbar('Done!')
           try {
             eval(jsCode['result']); // Execute code
           }
           catch(err) {
             console.log('error: ', err)
             console.log('type: ', typeof err.message)

            //  pass error through llm again
             fetch('/ask_llm', {
              method: 'POST',
              body: JSON.stringify({userInput: userValue, error: true, errorValue: err.message}),
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
              console.log('second try code to be executed: ', jsCode['result'])
              eval(jsCode['result'])
             })

             // try to execute code again
           }
         });

    }

  });

}

// Initialize on page load
window.onload = function() {
  setupAudioPlayer();
  //test_audio_editing_code();
  handleUserInputLLM();
};