import subprocess


class Subtitles:
    def __init__(self, input_video, subtitles_url, output_video):
        self.input_video = input_video
        self.subtitles_url = subtitles_url
        self.output_video = output_video

    def download_subtitles(self):
        subprocess.run(['wget', self.subtitles_url, '-O', 'subtitles.srt'])

    def integrate_subtitles(self):
        subprocess.run([
            'ffmpeg',
            '-i', self.input_video,
            '-vf', 'subtitles=subtitles.srt',
            '-c:a', 'copy',
            self.output_video
        ])

