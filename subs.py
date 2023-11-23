import subprocess


class Subtitles:
    def __init__(self, input_video, subtitles_url, output_video):
        self.input_video = input_video
        self.subtitles_url = subtitles_url
        self.output_video = output_video

    def download_subtitles(self):
        # Ejecutar comando para descargar subtitulos desde la Url especificada
        subprocess.run(['wget', self.subtitles_url, '-O', 'subtitles.srt'])

    def integrate_subtitles(self):
        # Ejecutar comando para integrar los subtitulos descargados como subtitles.srt en el video especificado:
        # ffmpeg -i input.mp4 -vf subtitles=subtitles.srt -c:a copy output.mp4
        subprocess.run([
            'ffmpeg',
            '-i', self.input_video,
            '-vf', 'subtitles=subtitles.srt',
            '-c:a', 'copy',
            self.output_video
        ])

