import subprocess
from subs import Subtitles


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

        # Exportar audio en MP3 mono
        mp3_mono_file = 'bbb_mono.mp3'
        subprocess.run(['ffmpeg', '-i', cut_video_file, '-vn', '-ac', '1', '-q:a', '2', mp3_mono_file])

        # Exportar audio en mp3 estéreo con bajo bitrate
        mp3_stereo_low_bitrate_file = 'bbb_stereo_low_bitrate.mp3'
        subprocess.run(['ffmpeg', '-i', cut_video_file, '-vn', '-q:a', '6', mp3_stereo_low_bitrate_file])

        # Exportar audio en codec aac
        aac_file = 'bbb_aac.aac'
        subprocess.run(['ffmpeg', '-i', cut_video_file, '-vn', '-c:a', 'aac', aac_file])

        # Fusionar en un contenedor mp4
        subprocess.run(['ffmpeg', '-i', cut_video_file, '-i', mp3_mono_file, '-i', mp3_stereo_low_bitrate_file, '-i',
                        aac_file, '-filter_complex',
                        "[0:v]concat=n=1:v=1:a=0[vout];[1:a][2:a][3:a]concat=n=3:v=0:a=1[aout]",
                        '-map', "[vout]", '-map', '[aout]', '-c:v', 'libx264', '-c:a', 'aac', output_file])

        # Limpiar archivos temporales
        # subprocess.run(['rm', cut_video_file, mp3_mono_file, mp3_stereo_low_bitrate_file, aac_file])

    def get_num_tracks(self, input_file):
        result = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'a', '-show_entries',
                                 'stream=index,codec_name', '-of', 'csv=p=0', input_file], text=True,
                                capture_output=True)

        num_tracks = len(result.stdout.strip().split('\n'))

        if num_tracks > 0:
            print(f"The MP4 container contains {num_tracks} audio track(s):")
        else:
            print(f"The MP4 container does not contain any audio track")


input_video = 'BBB.mp4'
output_video = 'output_cut.mp4'
output_video2 = 'output_contaniner.mp4'

# Crear instancia de la clase s2
s2class1 = s2(input_video)

while True:
    print("\nChoose a method to execute:")
    print("1. Cut and Analyze Video")
    print("2. Create New Container")
    print("3. Get number of tracks from a container")
    print("4. Add subtitles to video")
    print("0. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        s2class1.cut_and_analyze_video(output_video)
    elif choice == '2':
        s2class1.create_new_container(output_video2)
    elif choice == '3':
        s2class1.get_num_tracks(output_video2)
    elif choice == '4':
        input_video = "BBB.mp4"
        subtitles_url = "https://www.opensubtitles.com/download/813CC8487AFDAC6E7B90F52225A78F11900640E04D38972AD23EDD8C5A6429C51890988AEBBB4C8AEFAB2D2C86A0F64318481482037824128FFA8B9C3F2791440FDE016FF4EB25A47B3C923E2582227EB49D05EC5938AF39F27FCB1823C61F1FC1B57CB367AF473B0D431EF5BBC4D05F90FAAB33D7D569C510A882CA2AA039AADE195A4FA218FCEBFE111FC6552A99C9BDF606C126535349619B93D5C4F68753D4F21762405B1C347CFFFC4BAEC52353AB45EBAD360C1E93F4EF742167A15D823237792EF83DE544017818C3D28A2AF7C8468C333F20B0930AD46BBD0F0D6EDC36B1312F0E55EF72/subfile/big_buck_bunny.eng.srt"  # Replace with the subtitles URL

        output_video = "BBB_subtitles.mp4"

        subtitle_processor = Subtitles(input_video, subtitles_url, output_video)

        subtitle_processor.download_subtitles()

        subtitle_processor.integrate_subtitles()
    elif choice == '0':
        print("Exiting program.")
        break
    else:
        print("Invalid choice. Please enter 0, 1, or 2.")
