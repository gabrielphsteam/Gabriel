---
name: video-use
description: Edit and process video files with ffmpeg (trim, cut, merge, crop to vertical, add captions, extract audio, compress, change speed). Use when the user asks to edit, convert, shorten or reformat a video.
---

# Video Use

## Rules
- Never overwrite the original. Write results to a new file, for example `name_edit.mp4`.
- Check the file first: `ffprobe -v error -show_format -show_streams in.mp4`.
- Confirm ffmpeg exists (`which ffmpeg`); install if missing and allowed.
- For H.264 use `-c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p -c:a aac -movflags +faststart` unless the user asks for best quality.

## Recipes
- **Trim** (re-encode for accuracy): `ffmpeg -ss 00:00:10 -to 00:00:25 -i in.mp4 out.mp4`
- **Fast cut without re-encode**: `ffmpeg -ss 10 -to 25 -i in.mp4 -c copy out.mp4` (cuts land on keyframes)
- **Merge clips**: list files in `list.txt` as `file 'a.mp4'`, then `ffmpeg -f concat -safe 0 -i list.txt -c copy out.mp4` (same codec and size required)
- **Vertical 9:16 crop**: `ffmpeg -i in.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920" out.mp4`
- **Burn subtitles**: `ffmpeg -i in.mp4 -vf "subtitles=subs.srt" out.mp4`
- **Extract audio**: `ffmpeg -i in.mp4 -vn -c:a libmp3lame -q:a 2 out.mp3`
- **Compress**: raise `-crf` (23 to 28) and downscale with `-vf scale=1280:-2`
- **Speed**: `-filter:v "setpts=0.5*PTS" -filter:a "atempo=2.0"`
- **GIF**: `ffmpeg -i in.mp4 -vf "fps=12,scale=480:-1" out.gif`

## Finish
Verify the output plays (check duration and streams with ffprobe), report file size and what changed, and deliver the file to the user.
