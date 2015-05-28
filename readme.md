# Word Level Lyrics Aligner
## What is it?
The Word Level Lyrics Aligneris a lyrics aligner that takes audio file and its corresponed lyrics subtitle as input. 

Except two sample songs -- "Creep" and "Blank Space", all other subtitles are fetched randomly through MusiXmatch **[API](https://www.musixmatch.com)**.


## Dependencies
Need **[HTK](http://htk.eng.cam.ac.uk/)** and **[SoX](http://sox.sourceforge.net/)** to work. 
Required Python Libraries: **[Python wrap of MusiXmatch API](https://github.com/utstikkar/pyMusiXmatch)**, **[musicplayer](https://pypi.python.org/pypi/musicplayer)**.

Please install these tools on your own computer.

## Get it Run
Run main.py or `python dir/to/folder/main.py`
Choose a random song to start. Subtitle is automatically downloaded. Please make sure you have its corresponding .wav file.

To get evaluation of result, edit last line in eval.py, change `eval_song("data/vocal-Creep")` to `eval_song(dir-to your-audio-without-".wav")`, as long as you have .reference, .result, .subtitle files with the same name.

## Platform
OS X tested