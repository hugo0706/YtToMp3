from youtubesearchpython import VideosSearch
from unicodedata import normalize
import pytube
import os,sys,re

class bcolors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'
    FAIL = '\033[91m'

def normalizar(text):
    text = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1",normalize( "NFD", text), 0, re.I)       
    text = normalize( 'NFC', text)
    return text

def run():
    
    try:        
        f= open(sys.argv[1],'r', encoding='utf-8')
    except:
        print("Error: Ruta no encontrada")
        sys.exit()
    for line in f:
        name= normalizar(line.rstrip('\n')) + "\n"
        if name == "\n": continue
        else:
            try:   
                
                videosSearch = VideosSearch(name, limit = 2)
                video_url = videosSearch.result()['result'][0]['link']  
                video = pytube.YouTube(video_url).streams.filter(only_audio=True).first()
            
                out_file = video.download(output_path='./'+sys.argv[2]+'/')
                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp3'
                os.rename(out_file, new_file)
                print(name + bcolors.OKGREEN + "Descargado ->" + video.default_filename + bcolors.ENDC)
            except FileExistsError:
                print(bcolors.WARNING + "ERROR: Cancion Repetida"+ bcolors.ENDC )
                continue
            except: 
                print(bcolors.FAIL + "ERROR: Cancion no encontrada" + bcolors.ENDC)
                continue            
                    
if __name__=='__main__':
    run()
