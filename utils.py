from shazamio import Shazam
import os
import requests


async def media_shazaming(filename):
    shazam = Shazam()
    shazaming = await shazam.recognize_song(filename)
    
    if shazaming.get('track', None):
        title = shazaming.get('track').get('title')
        subtitle = shazaming.get('track').get('subtitle')
        result = [title, subtitle]
    
        
        if shazaming['track']['hub'].get("actions", False):
            audio_url = shazaming['track']['hub']['actions'][-1]['uri']
            result_audio = await download_audio_by_url(audio_url, title, subtitle)
            result.append(result_audio)
            
        return result


async def download_audio_by_url(url, title, subtitle):
    r = requests.get(url, stream=True)
    filename = f"{title} - {subtitle}.mp3"
    with open(filename, mode='wb') as f:
        f.write(r.content)

    return filename
    

async def delete_user_media(user_id):
    files = os.scandir()
    for f in files:
        if str(user_id) in f.name:
            os.remove(f.name)