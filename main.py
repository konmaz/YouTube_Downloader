import PySimpleGUI as sg
import re
import urllib

def get_video_id(youtube_url):
    regex = re.compile(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?(?P<id>[A-Za-z0-9\-=_]{11})')

    match = regex.match(youtube_url)

    if not match:
        print('no match')
    return(match.group('id'))
def get_video_thumb(yt_id):
    return 'http://img.youtube.com/vi/'+yt_id+'/maxresdefault.jpg'
    
image_elem = sg.Image(filename='button.png')

   # Add a little color to your windows
# All the stuff inside your window. This is the PSG magic code compactor...

layout = [  [sg.Image(filename="logo.png",background_color='#3a3a3a',pad=(25,25,25,25))],
            [image_elem],
            [sg.Text('Enter something on Row 2'), sg.InputText(key="txt_url")], # URL box
            [sg.Button(image_filename="button.png",button_color=('#3a3a3a', '#3a3a3a'),border_width=0,tooltip="Download",key='btn_dwn')], # download button
            
            
           

            [sg.OK(), sg.Cancel()]]

# Create the Window
sg.theme_background_color('#3a3a3a')


window = sg.Window('Window Title', layout,finalize=True,size=(550,500))

# Event Loop to process "events"
while True:             
    event, values = window.read()
    if event in (None, 'Cancel'):
        break
    elif event in 'btn_dwn':
        #url = values['txt_url'];
        #video_id =  (get_video_id(url))
        #print (get_video_thumb(video_id))
        image_elem.Update(filename='logo.png') 
        

window.close()