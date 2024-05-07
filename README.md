# Basic usage

1. Copy the timestamps from a YouTube comment.
2. Make sure they are well-formatted before proceeding (see below)
3. Run the script on this input:

    ```
    $ python comment_to_cuefile.py
    copy+paste comment below, then press Ctrl+D
    <paste the comment here>
    <track list will be printed>
    ```

4. Copy the outputted tracks into a CUE file, adding required tags at the top such as `FILE`.
5. Use the finished CUE file to split a downloaded video into its songs.

# Well-formatted timestamp comments

A well-formatted timestamp comment meets these requirements:
1. Each timestamp/song fits on one line (empty lines are fine, and will be ignored)
2. Each line takes the format {timestamp} {song} {artist}
3. There is a separator between timestamp and song that is common between all lines
4. There is also a common separator between song and artist (it may be a different separator than above)
5. No timestamps start later than 1:39:59 (99 minutes 59 seconds). This seems to be a limitation of CUE files.

## Examples of well-formated timestamps



## Examples of badly-formatted timestamps

# Input and output to files

# Examples of valid and invalid 
# how to run this script:
# 1. copy the timestamps in a YouTube comment.
# 2. make sure they are well-formatted. that means this:
#    a. each line should be its own song
#    b. each line should be of the format {timestamp} {song} {artist}
#    c. there should be consistent separators between timestamp and song, and between song and artist (the same for each line)
#    d. if any timestamp has a value higher than 1:39:59 (99 minutes and 59 seconds), this won't work--CUE files don't seem to support that.
# 3. Say that the separator between timestamp and song is A, and the one between song and artist is B.
#    then, you will run this script as
#    
#       python comment_to_cuefile.sh 