try:
    import json
    import os
    import re
    import sys
    from pydub import AudioSegment
    from moviepy.editor import AudioFileClip, ColorClip
except ImportError:
    print("Please install the following packages:")
    print("json")
    print("os")
    print("pydub")
    print("moviepy")
    exit()

class VideoCreator:

    files: list
    output: str

    def __init__(self, files, output):
        self.files = files
        self.output = output

    def create_video(self):
            
        if not self.output:
            print("No output given", file=sys.stderr)
            exit(1)

        if not self.files:
            print("No tracks marked for inclusion. Exiting.", file=sys.stderr)
            exit(1)

        pattern = re.compile("\.mp4$", re.IGNORECASE)

        if not pattern.findall(self.output):
            print("Output is not an mp4 file", file=sys.stderr)
            exit(1)

        for track_file in self.files:
            if not os.path.exists(track_file):
                print(f"Track file {track_file} does not exist. Exiting.", file=sys.stderr)
                exit(1)

        try:
            output_mp4 = self.output
            output_wav = pattern.sub(".wav", output_mp4)

            print(f"Writing to {output_wav} and {output_mp4}")

            combined_track = AudioSegment.empty()
            for track_file in self.files:
                audio = AudioSegment.from_file(track_file, format="pcm", frame_rate=44100, channels=2, sample_width=2)
                combined_track += audio

            combined_track.export(output_wav, format="wav")

            audio_clip = AudioFileClip(output_wav)
            video_clip = ColorClip(size=(720, 576), color=(0,0,0), duration=audio_clip.duration)
            video_clip = video_clip.set_audio(audio_clip)
            video_clip.write_videofile(output_mp4, fps=24)
        except:
            print(f"Error creating wav or mp4 file", file=sys.stderr)
            exit(1)