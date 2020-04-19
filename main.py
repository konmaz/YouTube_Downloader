import PySimpleGUI as sg
import re
import urllib
import requests
from PIL import ImageTk
import youtube_dl


def get_video_id(youtube_url):
    regex = re.compile(
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?(?P<id>[A-Za-z0-9\-=_]{11})')

    match = regex.match(youtube_url)

    if not match or youtube_url is None:
        return False
    else:
        return(match.group('id'))


def get_thumb_file(yt_video_id):
    url = 'http://img.youtube.com/vi/'+yt_video_id+'/maxresdefault.jpg'
    import requests
    from PIL import Image

    response = requests.get(url, stream=True)
    response.raw.decode_content = True
    image = Image.open(response.raw)

    if image.size == (120, 90):  # The Image was not found
        url = 'http://img.youtube.com/vi/'+yt_video_id+'/hqdefault.jpg'
        response = requests.get(url, stream=True)
        response.raw.decode_content = True
        image = Image.open(response.raw)

    # Resize image to fit in the window
    image = image.resize((460, 258), resample=1)
    # return image
    return ImageTk.PhotoImage(image)


def get_video_tile(yt_video_id):
    r = requests.get(
        'https://noembed.com/embed?url=https://www.youtube.com/watch?v='+yt_video_id)

    sg.Print(r.json())
    try:
        return (r.json()['title'])
    except KeyError:
        return ' '


layout = [[sg.Image(filename="logo.png", background_color='#3a3a3a', pad=(25, 25, 25, 25))],

          [sg.Image(filename='placeholder_thumbnail.png', pad=(
              25, 10), background_color='#3a3a3a', key='img_thumb')],  # Video Thumbnail

          [sg.Text(text='Title : ', pad=(30, (1, 18)), font=(
              'Product Sans', 14), size=(41, 2), background_color='#3a3a3a', tooltip="Video Title", key='txt_title')],  # Video Title

          [sg.InputText(font=('Product Sans Light', 13), background_color='#6d6d6d', text_color='white', size=(
              45, 0), pad=(28, 5), tooltip="Video URL", justification='center', enable_events=True, key="txt_box_url")],  # URL text box

          [sg.Button(image_filename="button.png", button_color=('#3a3a3a', '#3a3a3a'),
                     border_width=0, tooltip="Download", pad=((30, 5), 20), key='btn_dwn'),  # Download Button

           sg.Column([
               [sg.Radio('Audio', 'RD_DWNL_TYPE', background_color='#3a3a3a', font=(
                   'Product Sans Light', 13), default=True, enable_events=True, key='btn_rd_audio')],

               [sg.Radio('Video (Coming Soon)', 'RD_DWNL_TYPE', background_color='#3a3a3a', enable_events=True,
                         font=('Product Sans Light', 13), key='btn_rd_video', disabled=True, tooltip="Coming Soon")]],

               pad=(0, 15), background_color='#3a3a3a'),  # Radio Buttons


           sg.Combo(['1080p', '720p', '480p'], default_value='1080p',
                    visible=False, key='combo_quality', disabled=True)  # Quality Pressets DISABLED for now
           ],
          ]


# Create the Window
sg.theme_background_color('#3a3a3a')


window = sg.Window('YouTube Downloader', layout, finalize=True, size=(
    550, 700), icon="icon.ico")
old_value = ''
sg.Print('Start Debug Window')
# Event Loop to process "events"
while True:
    event, values = window.read()
    if event in (None, 'Cancel'):
        break
    url = values['txt_box_url']
    video_id = (get_video_id(url))
    if event in 'btn_dwn':  # EVENT Download Button was clicked

        if (video_id != False):  # If the text box url contains a valid video URL
            if (window['btn_rd_audio']):
                # Download Audio
                path = sg.PopupGetFile(
                    'Αποθήκευση...', no_window=True, save_as=True, file_types=(("Mp3 Files", "*.mp3"),))
                sg.Print("Path : "+path)
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                        
                    }], }

                sg.Print('Download Audio')
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_id])

            sg.Print('Download Button was clicked')

    elif event in 'txt_box_url':  # EVENT txt_box_url Value Was Changed
        if old_value != values['txt_box_url']:
            sg.Print('The value was changed')
            old_value = values['txt_box_url']

            if (video_id != False):  # If the text box url contains a valid video URL

                window.find_element('txt_title').Update(
                    value='Title : '+get_video_tile(video_id))  # Update Title Text
                window.find_element('img_thumb').Update(
                    data=get_thumb_file(video_id))  # Update Thumbnail Image

    sg.Print('Event :', event, '\nValue :', values)


window.close()
