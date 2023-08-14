"""Handles user input."""

import pickle

def load_embeddings(sotre_name, path):
    with open(f"{path}/faiss_{sotre_name}.pkl", "rb") as f:
        VectorStore = pickle.load(f)
    return VectorStore

# generate the query for the llm
def get_query(user_input):
    query = f'''You are a sound engineer. You are also a coding bot that only generates executable code. You have been given an audio file in the form of a wavesurfer object.
            The user has asked you to {user_input}.
            Write JavaScript code to do what the user has asked.'''
            
    add_query = ''' Here is some code that might help:
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

            /* action functions */

            function changeVolume(amount) {
            // change volume here
            const currentVolume = wavesurfer.getVolume();
            const newVolume = currentVolume + amount;
            const clampedVolume = Math.max(0, Math.min(1, newVolume));
            wavesurfer.setVolume(clampedVolume);
            console.log('Old volume: ', currentVolume);
            console.log('New volume: ', clampedVolume);
            }

            function changeSpeed(amount) {
            // change speed here
            const currentSpeed = wavesurfer.getPlaybackRate();
            const newSpeed = currentSpeed + amount;
            const clampedSpeed = Math.max(0.5, Math.min(4, newSpeed));
            wavesurfer.setPlaybackRate(clampedSpeed);
            console.log('Old speed: ', currentSpeed);
            console.log('New speed: ', clampedSpeed);
            }
            
            Make sure to only provide full code that can be immediately executed.'''
    
    query = query + add_query
              
    return query

if __name__ == '__main__':
    print('Running handle_user_input.py...')
    
    
    
    
    
    
    
    
    
