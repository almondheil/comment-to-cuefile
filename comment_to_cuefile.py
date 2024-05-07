# convert.py
# convert from a list of timestamps (like in youtube comments) to a .cue file
# almond Heil
# see README for how to run this script

import argparse
import sys


class timestamp:
    """
    A timestamp in the format mm:ss:ff (minutes seconds frames).
    """
    def __init__(self, minutes: int, seconds: int, frames: int = 0):
        if minutes < 0 or minutes > 99:
            print("ERROR: timestamp minutes must be between 0 and 99")
            exit(1)
        if seconds < 0 or seconds > 59:
            print("ERROR: timestamp seconds must be between 0 and 59")
            exit(1)
        if frames < 0 or frames > 75:
            print("ERROR: timestamp frames must be between 0 and 75")
            exit(1)
        
        self.minutes = minutes
        self.seconds = seconds
        self.frames = frames
        
    def __str__(self):
        res = "{:02d}:{:02d}:{:02d}"
        return res.format(self.minutes, self.seconds, self.frames)
    
    
class song:
    """
    A song with a timestamp, title, and author.
    """
    def __init__(self, timestamp: timestamp, title: str, author: str):
        self.timestamp = timestamp
        self.title = title
        self.author = author
        

def parse_timestamps(timestamps: str, first_sep: str, second_sep: str, author_before_title: bool = False) -> list[song]:
    """
    Parse a string containing song timestamps into a list of song objects.
    
    :param timestamps: Input timestamp string, where each line is one song
    :param first_sep: Separator between timestamp and first item (title or author)
    :param second_set: Separator between first and second item (title and author, or vice versa)
    :param author_before_title: Whether the author appears before the title on each line. If left false, title appears before author on each line.
    """
    songs = []
    for line in timestamps.splitlines():
        # skip this line if it is empty
        if line.strip() == "":
            continue
        
        # split into either 2 or 3 items
        time_str, rest = [s.strip() for s in line.split(first_sep, 1)]
        second, *third = [s.strip() for s in rest.split(second_sep, 1)]
        
        # parse time, which will always appear first
        time_lst = time_str.split(":")
        if len(time_lst) == 3:
            # this time has hours, convert them to minutes
            hrs = int(time_lst[0])
            mins = int(time_lst[1])
            secs = int(time_lst[2])
            time = timestamp(60*hrs + mins, secs)
        elif len(time_lst) == 2:
            mins = int(time_lst[0])
            secs = int(time_lst[1])
            time = timestamp(mins, secs)
        else:
            print(f"ERROR: time is not hours:min:sec or min:sec format, it is {time_str}")
            exit(1)
        
        if author_before_title:
            # if the order goes time-author-title
            # if there is no third item, use "Untitled" as the song title
            s = song(time, third[0] if len(third) != 0 else "Untitled", second)
        else:
            # if the order goes time-title-author
            # if there is no third item, use None as the author
            s = song(time, second, third[0] if len(third) != 0 else None)
            
        songs.append(s)
    return songs

def print_tracks_as_cuesheet(songs: list[song], file=None):
    """
    Print a list of tracks in a Cuesheet format.
    
    :param songs: A list of song objects
    :param file: Output file to print to. If None, will print to stdout.
    """
    for num, track in enumerate(songs):
        # always print which track number this is, and the title
        print(f"\tTRACK {(num + 1):02d} AUDIO", file=file)
        print(f"\t\tTITLE \"{track.title}\"", file=file)
        
        # author may or may not be defined
        if track.author:
            print(f"\t\tPERFORMER \"{track.author}\"", file=file)
            
        # add :00 onto the timestamp, for the frames
        print(f"\t\tINDEX 01 {track.timestamp}", file=file)

def main():
    # set up parser with all the options we need
    parser = argparse.ArgumentParser(description="Parse a YouTube comment to a .cue track list, where each line of the comment holds a timestamp, song title, and author")
    parser.add_argument("first_sep", help="Separator between first and second parts of line (eg \" \" or \"-\")")
    parser.add_argument("second_sep", help="Separator between second and third parts of line (eg \"-\" or \"by\")")
    parser.add_argument("-i", "--infile", help="If used, read timestamp comment from this file. Otherwise, use stdin.")
    parser.add_argument("-o", "--outfile", help="If used, append track list to this file. Otherwise, print to stdout.")
    parser.add_argument("-r", "--reverse-order", action="store_true", help="If enabled, expect lines of the form {timestamp} {author} {title}. Otherwise, expect to {timestamp} {title} {author}")

    # attempt to parse args (if invalid args were provided, will print a help message)
    args = parser.parse_args()
    
    # open the input file if one was provided
    if args.infile:
        infile = open(args.infile, "r")
    else:
        infile = sys.stdin
        print("copy+paste comment below, then press Ctrl+D")
        
    # read the contents of the infile into one big string
    timestamps = infile.read()
    infile.close()
    
    # parse the timestamps from that string into a list of songs
    songs = parse_timestamps(timestamps, args.first_sep, args.second_sep, author_before_title=args.reverse_order)
    
    # print those songs to the output file as a list of Cuesheet tracks
    if args.outfile:
        with open(args.outfile, "a") as outfile:
            print_tracks_as_cuesheet(songs, file=outfile)    
    else:
        print_tracks_as_cuesheet(songs)
    
    
if __name__ == "__main__":
    main()