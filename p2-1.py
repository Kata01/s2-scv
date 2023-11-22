import subprocess


class s2:
    def __init__(self, input_file):
        self.input_file = input_file

    def cut_and_analyze_video(self, output_file):
        # Cortar 9 primeros segundos de video con el comando "ffmpeg -i input.mp4 -t 9 output.mp4"
        subprocess.run(['ffmpeg', '-i', self.input_file, '-t', '9', output_file])

        # Obtener video con vectores de movimiento y macrobloques con el comando "ffmpeg -flags2 +export_mvs -i
        # input.mp4 -vf codecview=mv=pf+bf+bb output.mp4"
        subprocess.run(['ffmpeg', '-flags2', '+export_mvs', '-i', output_file, '-vf', 'codecview=mv=pf+bf+bb',
                        'output_analyzed.mp4', ])

        # Limpiar archivos temporales
        subprocess.run(['rm', output_file])

    def create_new_container(self, output_file):
        # Cortar 50 primeros segundos de video con el comando "ffmpeg -i input.mp4 -t 50 output.mp4"
        cut_video_file = 'bbb_50s.mp4'
        subprocess.run(['ffmpeg', '-i', self.input_file, '-t', '50', cut_video_file])

        # Step 2: Export BBB(50s) audio as MP3 mono track
        mp3_mono_file = 'bbb_mono.mp3'
        subprocess.run(['ffmpeg', '-i', cut_video_file, '-vn', '-ac', '1', '-q:a', '2', mp3_mono_file])

        # Step 3: Export BBB(50s) audio in MP3 stereo with a lower bitrate
        mp3_stereo_low_bitrate_file = 'bbb_stereo_low_bitrate.mp3'
        subprocess.run(['ffmpeg', '-i', cut_video_file, '-vn', '-q:a', '5', mp3_stereo_low_bitrate_file])

        # Step 4: Export BBB(50s) audio in AAC codec
        aac_file = 'bbb_aac.aac'
        subprocess.run(['ffmpeg', '-i', cut_video_file, '-vn', '-c:a', 'aac', aac_file])

        # Step 5: Package everything in a .mp4 with FFMPEG
        subprocess.run([
            'ffmpeg',
            '-i', cut_video_file,
            '-i', mp3_mono_file,
            '-i', mp3_stereo_low_bitrate_file,
            '-i', aac_file,
            '-filter_complex', f"[0:v][1:a][2:a][3:a]concat=n=4:v=1:a=1[vout][aout]",
            '-map', '[vout]',
            '-map', '[aout]',
            '-c:v', 'copy',
            '-c:a', 'aac',
            output_file
        ])

        # Limpiar archivos temporales
        subprocess.run(['rm', cut_video_file, mp3_mono_file, mp3_stereo_low_bitrate_file, aac_file])


input_video = 'BBB.mp4'
output_video = 'output_cut.mp4'
output_video2 = 'output_contaniner-mp4'

# Crear instancia de
s2class1 = s2(input_video)

while True:
    print("\nChoose a method to execute:")
    print("1. Cut and Analyze Video")
    print("2. Create New Container")
    print("0. Exit")

    choice = input("Enter your choice (0, 1, or 2): ")

    if choice == '1':
        s2class1.cut_and_analyze_video(output_video)
    elif choice == '2':
        s2class1.create_new_container(output_video2)
    elif choice == '0':
        print("Exiting program.")
        break
    else:
        print("Invalid choice. Please enter 0, 1, or 2.")