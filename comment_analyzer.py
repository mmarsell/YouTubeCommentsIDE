import os
import re
from googleapiclient.discovery import build
api_key = '<API KEY>'


yt_service = build('youtube','v3', developerKey=api_key)
request = yt_service.commentThreads().list(
        part='snippet',
        videoId='<videoID>',
        maxResults=100
    )

response = request.execute()
num = 0
for comment in response['items']:
    filepath = "outputfiles/output"+str(num)+".py"
    with open(filepath, "a", encoding="utf-8") as output_file:
        comment_text = comment['snippet']['topLevelComment']['snippet']['textDisplay']
        comment_text = comment_text.replace("&quot;", "\"").replace("<br />","\n").replace("&gt;", ">").replace("&lt;", "<").replace("&#39;", "'").replace("<i>", "_").replace("</i>", "_").replace("”","\"").replace("“","\"")
        comment_text = re.sub('<.*?>','', comment_text)
        output_file.write("try:\n")
        lines = str(comment_text).splitlines()
        for line in lines:
            if line != '\n':
                output_file.write("\t"+line +"\n")
        output_file.write("except:" + "\n \tprint(\"Not valid python code\")")
    num = num + 1

for script in os.listdir('outputFiles'):
    try:
        exec(open("outputFiles/"+script).read())
    except:
        print("Invalid python code or syntax")
    os.remove("outputFiles/"+script)
