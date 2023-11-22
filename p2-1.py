import subprocess

class VideoProcessor:
    def __init__(self, input_file):
        self.input_file = input_file

    def cut_and_analyze_video(self, output_file):
        # Step 1: Cut the video to the first 9 seconds
        subprocess.run(['ffmpeg', '-i', self.input_file, '-t', '9', output_file])

        # Step 2: Analyze the video for macroblocks and motion vectors
        subprocess.run([
            'ffmpeg',
            '-flags2', '+export_mvs',
            '-i', output_file,
            '-vf', 'codecview=mv=pf+bf+bb',
            output_video
            ,
        ])

# Example usage
input_video = 'BBB.mp4'
output_video = 'output_cut_and_analyzed.mp4'

# Create an instance of VideoProcessor
video_processor = VideoProcessor(input_video)

# Cut and analyze the video
video_processor.cut_and_analyze_video(output_video)
