import PySimpleGUI as sg
import re
import urllib
import requests
from PIL import ImageTk


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
    # Resize image to fit in the window
    image = image.resize((460, 258), resample=1)
    # return image
    return ImageTk.PhotoImage(image)


def get_video_tile(yt_video_id):
    r = requests.get(
        'https://noembed.com/embed?url=https://www.youtube.com/watch?v='+yt_video_id)
    return (r.json()['title'])


image_elem = sg.Image(filename='placeholder_thumbnail.png', pad=(
    25, 10), background_color='#3a3a3a',)  # Video Image PlaceHolder

text_elem = sg.Text(text='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi porta nulla a mi eleifend malesuada. A', pad=(30, (1, 18)), font=(
    'Product Sans', 14), size=(41, 2), background_color='#3a3a3a', tooltip="Video Title",)  # Video Title Placeholder

layout = [[sg.Image(filename="logo.png", background_color='#3a3a3a', pad=(25, 25, 25, 25))],
          [image_elem], [text_elem],

          [sg.InputText(key="txt_url", font=('Product Sans Light', 13), background_color='#6d6d6d', text_color='white', size=(
              45, 0), pad=(28, 5), tooltip="Video URL", justification='center')],  # URL text box

          [sg.Button(image_filename="button.png", button_color=('#3a3a3a', '#3a3a3a'),
                     border_width=0, tooltip="Download", key='btn_dwn', pad=(30, 20)),
            sg.Combo      (['1080p','720p','480p'],default_value='1080p')
                     
                     ]



          ]


# Create the Window
sg.theme_background_color('#3a3a3a')


window = sg.Window('Window Title', layout, finalize=True, size=(550, 700))

# Event Loop to process "events"
while True:
    event, values = window.read()
    if event in (None, 'Cancel'):
        break

    elif event in 'btn_dwn':
        url = values['txt_url']
        video_id = (get_video_id(url))

        if (video_id != False):  # if the text box is not empty
            text_elem.Update(value=get_video_tile(video_id))
            thumb = get_thumb_file(video_id)  # get thumbnail image
            image_elem.Update(data=thumb)  # update thumbnail


window.close()
