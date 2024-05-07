# Comment to Cuesheet

This is a python script that has the goal of converting from a YouTube comment with video timestamps for an album to a CUE sheet tracklist. It has some limitations due to the specifications of CUE sheet, such as not working with timestamps that happen after 1h40m (100 minutes). 

Once you run this script on a comment, you will have the tracks of a CUE sheet, which you can then flesh out to a full sheet. Then, it is possible to use the completed CUE sheet to split a downloaded audio file into its individual tracks for ease of listening and transfer.

# Basic usage

1. Find a YouTube comment with timestamps for each song in a video.

2. Make sure they are well-formatted. They should all follow the same order (either timestamp, track name, author or timestamp, author, track name), and there should be consistent separators between the three parts.

    See the [Examples](#examples) section or the [Formatting Specification](#formatting-specification) sections below for more info on how to tweak a timestamps comment to be formatted in a way the script can handle.

3. Run the script, specifying the separators that are used in that comment.

    ```
    python comment_to_cuefile.py "-" "by"
    ```

    With this example, you would then copy+paste the comment into the terminal and press Ctrl+D to confirm.

4. Copy the outputted tracks into a CUE sheet, adding [other required commands](https://en.wikipedia.org/wiki/Cue_sheet_(computing)#Essential_commands) at the top such as `FILE`.
   
5. Use the finished CUE sheet to split a downloaded album audio into its individual songs.

# Formatting Specification

Each line in a comment must be formatted in the same way, but it is possible for the script to work with two forms:

The default is `{timestamp} {author} {title}`.

The alternate order is `{timestamp} {author} {title}`. To use this ordering, pass the `-r` flag when running the script.

In both cases, there are two separators - between the timestamp and second item, and between the second and third. 

The first and second separator do not need to be the same (for lines formatted like "0:00 - Song by Author", your separators would be `"-"` and `"by"`), but each line must have the same separators as the others.

# Examples

For these examples, suppose your comment is formatted as follows:

```
0:00 - odoriko by Vaundy
3:48 - Loretta by ginger root
6:58 - natsuyo no magic by Indigo la End
11:58 - Nakaniwa no Shoujotachi by SHISHAMO
17:17 - aomi by Gesu no Kiwami otome
22:29 - Yume Utsutsu by Lamp
27:45 - Kokoro ni Kumo wo Motsu Shounen by Sunny Day Service
31:33 - Dancing in the rain by Meaningful stone 
35:31 - akogare by mitsume 
39:12 - Killer tune kills me by KIRINJI
43:23 - Good news is bad news by helsinki lambda club
47:31 - Graduation by HYUKOH
51:47 - Windy afternoon by Lamp
56:39 - Hatchi No Koi by Lamp
```

## Simplest example

By default, you would run this to process the comment, then paste it when prompted:

```
python comment_to_cuefile.py "-" "by"
```

## Input and output files

If you had pasted the comment into `comment.txt` to format it properly, you could run

```
python comment_to_cuefile.py -i comment.txt "-" "by"
```

If you instead want to append the outputted tracklist into your file `tracks.cue`, you could run

```
python comment_to_cuefile.py -o tracks.cue "-" "by"
```

The `-i` and `-o` flags can also be combined so you don't have to do any copy-pasting yourself.

```
python comment_to_cuefile.py -i comment.txt -o tracks.cue "-" "by"
```

## Less common comment formatting

### A space between the timestamp and the first field

It's perfectly okay if your comment is formatted with spaces as the first separator, because timestamps don't have spaces. 

> A space as the second separator won't work if there are songs with spaces in the title, but someone writing a timestamp comment probably won't use these because they are ambiguous to people reading the comment.

If your comment looks like this:

```
0:00 odoriko by Vaundy
3:48 Loretta by ginger root
6:58 natsuyo no magic by Indigo la End
11:58 Nakaniwa no Shoujotachi by SHISHAMO
17:17 aomi by Gesu no Kiwami otome
22:29 Yume Utsutsu by Lamp
27:45 Kokoro ni Kumo wo Motsu Shounen by Sunny Day Service
31:33 Dancing in the rain by Meaningful stone 
35:31 akogare by mitsume 
39:12 Killer tune kills me by KIRINJI
43:23 Good news is bad news by helsinki lambda club
47:31 Graduation by HYUKOH
51:47 Windy afternoon by Lamp
56:39 Hatchi No Koi by Lamp
```

You would run:

```
python comment_to_cuefile.py " " "by"
```

### Time-Author-Title order instead of Time-Title-Author

Pass the `-r` flag to signal to the script that the order of title and author will be flipped.

If your comment is formatted like:
```
0:00 - Vaundy, odoriko
3:48 - ginger root, Loretta
6:58 - Indigo la End, natsuyo no magic
11:58 - SHISHAMO, Nakaniwa no Shoujotachi 
17:17 - Gesu no Kiwami otome, aomi 
22:29 - Lamp, Yume Utsutsu
27:45 - Sunny Day Service, Kokoro ni Kumo wo Motsu Shounen
31:33 - Meaningful stone, Dancing in the rain
35:31 - mitsume, akogare 
39:12 - KIRINJI, Killer tune kills me
43:23 - helsinki lambda club, Good news is bad news
47:31 - HYUKOH, Graduation
51:47 - Lamp, Windy afternoon
56:39 - Lamp, Hatchi No Koi
```

You would run:

```
python comment_to_cuefile.py -r "-" ","
```