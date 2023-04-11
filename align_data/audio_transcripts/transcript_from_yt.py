import os
import tempfile
from pytube import YouTube
import openai
from pydub import AudioSegment


def download_youtube_video(url: str, temp_folder: str = None) -> str:
    if temp_folder is None:
        temp_folder = tempfile.gettempdir()
    
    try:
        yt = YouTube(url)
        video = yt.streams.filter(file_extension="mp3", progressive=True).get_highest_resolution()
        
        if video is None:
            raise Exception("No MP4 video found")
        
        output_path = os.path.join(temp_folder, video.default_filename)
        video.download(output_path)

        print(f"Video downloaded to {output_path}")
        return output_path
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None
    

def transcribe_long(video_path):

    song = AudioSegment.from_mp3(video_path)
    # PyDub handles time in milliseconds
    ten_minutes = 10 * 60 * 1000
    transcription_blocks = []

    #for each ~tenminute chunk, get the transcription
    for idx in range(0, len(song), ten_minutes):
        idx_end = min(idx+ten_minutes, len(song))

        #ten_min_chunk_name = "ten_" + video_path
        ten_min_chunk = song[idx:idx_end]
        #ten_min_chunk.export(ten_min_chunk_name, format="mp3")
        chunk_transcript = openai.Audio.translate("whisper-1", ten_min_chunk)#_name)
        transcription_blocks.append(chunk_transcript)
    
    return transcription_blocks






if __name__ == "__main__":
    url = input("Enter the YouTube video URL: ")
    video_path = download_youtube_video(url)
    transcription = transcribe_long(video_path)