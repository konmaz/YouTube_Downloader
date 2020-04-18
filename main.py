import PySimpleGUI as sg
import urllib
import urllib.parse as urlparse
def get_video_id(url):
    """Returns Video_ID extracting from the given url of Youtube
    
    Examples of URLs:
      Valid:
        'http://youtu.be/_lOT2p_FCvA',
        'www.youtube.com/watch?v=_lOT2p_FCvA&feature=feedu',
        'http://www.youtube.com/embed/_lOT2p_FCvA',
        'http://www.youtube.com/v/_lOT2p_FCvA?version=3&amp;hl=en_US',
        'https://www.youtube.com/watch?v=rTHlyTphWP0&index=6&list=PLjeDyYvG6-40qawYNR4juzvSOg-ezZ2a6',
        'youtube.com/watch?v=_lOT2p_FCvA',
      
      Invalid:
        'youtu.be/watch?v=_lOT2p_FCvA',
    """

    from urlparse import urlparse, parse_qs

    if url.startswith(('youtu', 'www')):
        url = 'http://' + url
        
    query = urlparse(url)
    
    if 'youtube' in query.hostname:
        if query.path == '/watch':
            return parse_qs(query.query)['v'][0]
        elif query.path.startswith(('/embed/', '/v/')):
            return query.path.split('/')[2]
    elif 'youtu.be' in query.hostname:
        return query.path[1:]
    else:
        raise ValueError
   # Add a little color to your windows
# All the stuff inside your window. This is the PSG magic code compactor...

layout = [  [sg.Image(filename="logo.png",background_color='#3a3a3a',pad=(25,25,25,25))],
            
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
        url = values['txt_url'];
        print (get_video_id(url))
        

window.close()