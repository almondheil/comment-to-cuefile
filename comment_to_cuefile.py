# convert.py
# convert from a list of timestamps (like in youtube comments) to a .cue file
# almond Heil
# see README for how to run this script

import argparse
import sys


class timestamp:
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
    def __init__(self, timestamp: timestamp, title: str, author: str):
        self.timestamp = timestamp
        self.title = title
        self.author = author
        

def parse_comment(comment: str, first_sep: str, second_sep: str, author_before_title: bool = False) -> list[song]:
    songs = []
    for line in comment.splitlines():
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

def print_tracks(songs: list[song], file=None):
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
    parser = argparse.ArgumentParser(description="Parse a YouTube comment to a .cue track list, where each line of the comment holds a timestamp, song title, and author")
    parser.add_argument("first_sep", help="Separator between first and second parts of line (eg \" \" or \"-\")")
    parser.add_argument("second_sep", help="Separator between second and third parts of line (eg \"-\" or \"by\")")
    parser.add_argument("-i", "--infile", help="If used, read timestamp comment from this file. Otherwise, use stdin.")
    parser.add_argument("-o", "--outfile", help="If used, append track list to this file. Otherwise, print to stdout.")
    parser.add_argument("-r", "--reverse-order", action="store_true", help="If enabled, expect lines of the form {timestamp} {author} {title}. Otherwise, expect to {timestamp} {title} {author}")

    args = parser.parse_args()
    
    if args.infile:
        infile = open(args.infile, "r")
    else:
        infile = sys.stdin
        print("copy+paste comment below, then press Ctrl+D")
        
    comment = infile.read()
    infile.close()
    
    songs = parse_comment(comment, args.first_sep, args.second_sep, author_before_title=args.reverse_order)
    if args.outfile:
        with open(args.outfile, "a") as outfile:
            print_tracks(songs, file=outfile)    
    else:
        print_tracks(songs)
    
if __name__ == "__main__":
    main()