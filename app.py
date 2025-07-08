from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from flask_cors import CORS

def get_video_id(url_link):
    return url_link.split("watch?v=")[-1]


def getValidate(textTrans):
    try:
        # print(textTrans)
        textarr = textTrans.split()
        return len(textarr)
      
    except Exception as e:
         return "not valid"

def gettrans(video_id):
    try:

    # List all available transcripts
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        lang = ''
        print("📋 Available Subtitles:")
        for transcript in transcript_list:
            lang = transcript.language_code
        print(lang)
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
        transcript_joined = " ".join([line['text'] for line in transcript])
        return transcript_joined
    except Exception as e:
       print(str(e))
       return "Error fetching transcript"


app = Flask(__name__)
CORS(app)

@app.route('/get-subtitles', methods=['POST'])
def get_subtitles():
    data = request.json
    url = data.get("url")
    if not url:
        return jsonify({"error": "Missing 'url' in request"}), 400

    try:
        video_id = get_video_id(url)
        transcript_text = gettrans(video_id)
        # getValidate(transcript_text)
        if getValidate(transcript_text) < 10000:
            return jsonify({"transcript":transcript_text})
        else:
            return jsonify({"transcript":"too long video"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/")
def hello_world():
    return "Bhai Dekh Garib hu."


if __name__ == "__main__":
    app.run(debug=False,host="0.0.0.0")
