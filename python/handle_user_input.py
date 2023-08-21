"""Handles user input."""

import pickle

# generate the query for the llm
def get_query(user_input, error, error_value=None):
    print('Error value: ', error_value)
    error_message = f'The below prompt was sent to you and this is the outputted error {error_value}. Try again, taking this error into consideration. Previous prompt: '
    
    query = f'''    
            You are a sound engineer. 
            You are also a coding bot that only generates executable code. 
            You have been given an audio file in the form of a wavesurfer.js object.
            The user has asked you to {user_input}.
            Think step by step.''
            
            Write JavaScript code to do what the user has asked. Check to make sure that the function you choose is actually part of the API you are using.
            Also, check that your code has: 1. a wavesurfer object and 2. a method that actually exists in the wavesurfer.js library.
            
            If the user asks to increase or decrease something or if you are adjusting a value, make sure you get the current value of that something.
            
            '''
            
    add_query = '''
            This is the code that sets up the wavesurfer object that you want to use:
            
            var wavesurfer = null;

            // sets up the waveform player
            function setupAudioPlayer() {
            wavesurfer = WaveSurfer.create({
                container: '#waveform',
                waveColor: '#4F4A85',
                progressColor: '#383351'//,
                //mediaControls: true
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
            Make sure to only provide full code that can be immediately executed.'''
    
    query = query + add_query
    
    if error: return error_message + query
    else: return query

if __name__ == '__main__':
    print('Running handle_user_input.py...')
    
    
    
    
    
    
    
    
    
