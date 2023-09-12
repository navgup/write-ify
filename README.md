# write-ify
A journaling app that plays music to match your mood

**Key Features**
- React frontend integrated with Flask backend
- Integrated with Spotify API following REST principles
- Spotify API used for OAuth (login) and to get user data, song recommendations, queue music and control playback
- User text is analyzed using BERT Emotion Detection model from HuggingFace (https://huggingface.co/j-hartmann/emotion-english-distilroberta-base)
- Emotional parameters from BERT model are sent to trained linear regression model on backend, which predicts song attributes (instrumentalness, valence, volume, etc). to feed into Spotify Recommendation algorithm

**How to use**
1. Hit the "Login to Spotify" button and authorize Writify to access your listening preferences (necessary to recommend songs) and control playback
2. Make sure you are actively listening to Spotify on a device -- playback can't be controlled if you're not playing a song!
3. Type whatever is on your mind! More "emotional" content will be picked up better by the NLP model and lead to songs that match your mood.
4. Every minute, Writify will re-analyze your writing and automatically queue and play you a new song
