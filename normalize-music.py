import pydub
from pydub import AudioSegment
import argparse
import glob
from pathlib2 import Path
import os
import time 

#TODO: Add option to declare target dBFS directly; for reference current flipphone audio target is -24.43732842927202

parser = argparse.ArgumentParser()
parser.add_argument('--files', '-f', help='What files to operate on (glob). By default: "*.mp3", i.e. all files in the present directory ending with the extension .mp3.', default='*.mp3')
parser.add_argument('--ref', '-r', help='Reference file to match the average volume of (by dBFS). If none given, uses the file in the directory with the lowest average volume')
parser.add_argument('--adjust', '-a', help='After normalizing volumes, what dB to adjust each file by. Default: 0.0', default=0.0, type=float)
parser.add_argument('--output', '-o', help='Where to put the output files. If a directory is given, clones files into analogous locations within that directory ("<filepath>" --> "<--output><filepath>"). By default, none (overwrites existing files)', default="./output/")
parser.add_argument('--skip-existing', '-s', help='Whether or not to skip files where the output path already contains a file. False by default (i.e. overwrites existing files)', action="store_true")
parser.add_argument('--only-adjust', help="If specified, doesn't compare and normalize, only applying the desired adjustment", action="store_true")
parser.add_argument('--ignore-directories', '-i', help="Ignore relative directory information and place files directly in output, i.e. 'Downloads/folder/directory/music.mp3' -> 'output/music.mp3' instead of 'output/Downloads/folder/dirctory/music.mp3'", action="store_true")
args = parser.parse_args()
target_files_glob:str = args.files
files = glob.glob(target_files_glob)
# print(files)
num_files = len(files)
# num_files = 4
output_path:str = args.output
db_adjust:float = args.adjust


### Identify Target Loudness (dBFS)
target_loudness:float

ref_filepath = args.ref
if ref_filepath is None:
    min_loudness = 0
    for i in range(num_files):
        next_filepath:str = files[i]
        print(next_filepath)
        song = AudioSegment.from_mp3(next_filepath)
        loudness = song.dBFS
        print(loudness)
        min_loudness = min(min_loudness, loudness)
    target_loudness = min_loudness
else:
    ref_song = AudioSegment.from_mp3(ref_filepath)
    print("Matching loudness of: " + ref_filepath)
    target_loudness = ref_song.dBFS
print("Target loudness: ",target_loudness, ", adjusted by: ", db_adjust)
# exit()

### Adjust each song to match target loudness
for i in range(num_files):
    next_filepath:str = files[i]
    song_output_path:str
    if args.ignore_directories:
        song_output_path  = output_path+Path(next_filepath).stem
    else:
        song_output_path = output_path+next_filepath
    
    song_output:Path = Path(song_output_path)

    if song_output.exists() and args.skip_existing:
        print(f"[{i+1} / {num_files}] Skipping: "+song_output_path+" (Target file already exists)")
        continue
    try:
        
        next_song:AudioSegment = AudioSegment.from_mp3(next_filepath)
        target_gain = target_loudness - next_song.dBFS + db_adjust
        if args.only_adjust:
            target_gain = db_adjust
        next_song_adjusted = next_song.apply_gain(target_gain)
        #Export
        

        if not Path(song_output_path).exists():
            
            dir_to_make = "/".join(Path(song_output_path).parts[:-1])
            os.makedirs(dir_to_make,exist_ok=True)
            # Path(song_output_path).mkdir()
            Path(song_output_path).touch()
        print(f"[{i+1} / {num_files}] Exporting: "+song_output_path+" ... ")
        next_song_adjusted.export(song_output_path, format="mp3")
    except:
        print(f"[{i+1} / {num_files}] Could not Export: "+song_output_path+" ... ")
    
