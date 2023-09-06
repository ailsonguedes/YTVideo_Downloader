import os
from flask import Flask, request, render_template, send_from_directory
from pytube import YouTube
from moviepy.editor import VideoFileClip

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        
        try:
            yt = YouTube(url)
            stream = yt.streams.get_highest_resolution()
            
            video_title = yt.title
            original_filename = f"{video_title}.mp4"
            #converted_filename = f"{video_title}_converted.mp4"

            # Baixar o vídeo em seu formato original
            stream.download(output_path="downloads", filename=original_filename)
            
            # Oferecer o download do arquivo convertido
            response = send_from_directory("downloads", original_filename, as_attachment=True)
            
            return response 
              
        except Exception as e:
            return f"Erro: {str(e)}"
        
    return render_template("index.html")

if __name__ == "__main__":
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    app.run(debug=True)
    