from pytube import YouTube

link = YouTube("https://www.youtube.com/watch?v=kcudEcmW1SE&list=PLy6N_9yB8Qwy6LL0J7zLUyW8XNX-BPeDl&index=1")

song = link.streams.get_audio_only()
song.download()
