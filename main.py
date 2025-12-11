from youtube_subtitle import download_english_subtitles
from vtt_convert import vtt_to_text
from sentiment_analysis import analyze_file
import glob
import os

def analyze_youtube_video(urls: list):

    # Download eng subtitle and save .vtt fies on subs folder
    for url in urls:
        download_english_subtitles(url)

    # make .txt files
    vtt_files_path = ["./subs/" + file.split("\\")[1] for file in glob.glob("subs/*.vtt") ]
    for file in vtt_files_path:
        vtt_to_text(file)

    # analyze .txt files
    txt_files_path = ["./subs/" + file.split("\\")[1] for file in glob.glob("subs/*.txt") ]
    for path in txt_files_path:
        if not os.path.exists(path):
            print(f"File not found: {path}")
        else:
            res = analyze_file(path)
            print(res)




if __name__ == "__main__":
    urls = input("Enter YouTube video URLs: ").strip().split()
    if urls:
        analyze_youtube_video(urls)
    else:
        print("No URL provided.")