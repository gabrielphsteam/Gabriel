---
name: video-lens
description: Analyze a video file or link and report what it contains (summary, key moments, spoken content, on-screen text, structure). Use when the user shares a video and asks what it says, for a summary, timestamps, or feedback on it.
---

# Video Lens

## Workflow
1. **Get the video**: a local file, or a URL the user provided. If it cannot be downloaded, ask the user to attach the file.
2. **Inspect**: `ffprobe -v error -show_format -show_streams <file>` for duration, resolution, fps, audio.
3. **Transcript**: if a speech-to-text tool is installed (for example `whisper`), transcribe with timestamps. If not, say so and rely on frames and any subtitle track (`ffmpeg -i in.mp4 -map 0:s:0 subs.srt`).
4. **Frames**: sample frames to view them, for example one every N seconds:
   `ffmpeg -i in.mp4 -vf "fps=1/5,scale=640:-1" frames/f_%03d.jpg`
   Read the images to describe scenes, on-screen text and visual style. Add scene-change frames with `select='gt(scene,0.35)'` for long videos.
5. **Synthesize**.

## Output
- One-paragraph summary
- Timeline of key moments with timestamps
- Spoken points and on-screen text
- If asked: feedback on hook (first 3 seconds), pacing, clarity, calls to action

## Rules
- Separate what you saw or heard from what you infer.
- Do not invent audio you could not transcribe.
- Keep temporary frames and audio in a scratch folder, not in the repo.
