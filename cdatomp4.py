import youtube_dl
import sys
listamp4=dict()
for i in listamp4.keys():
    print(i)
    del listamp4[i]

ydl_opts = {
    'quiet': True
}
def cdatomp4(link):
    try:
        listamp4.clear()
        print("cleared")
    except:
        None
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    	meta = ydl.extract_info(link, download=False) 
    try:
        for i in range(len(meta['formats'])):
    	    listamp4[meta['formats'][i]['height']]=meta['formats'][i]['url']
    except:
    	listamp4["idk"]=meta['url']
    return(listamp4)
for i in sys.argv:
    if "http" in i:
        print(cdatomp4(i))