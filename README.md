Designed Python Environment \(But this isn't a super complicated script, so realistically other versions should work\):
Python 3.12.3, pydub 0.25.1

Usage: Run script with flag -f specifying a glob path of files to copy (e.g. "*.mp3" for all mp3 files in the current directory), and then optionally:
  - flag -r specifying a song to match the volume (dBFS) of
  - flag -a to adjust the output by a certain dB (i.e. positive to increase, negative to decrease)
  - flag -o to specify where to clone the adjusted-volume files to
  - flag -i to ignore directory information, and just put all the files directly in the output folder
  - flag -s to skip files where a the target output file already exists
