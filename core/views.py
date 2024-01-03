from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
from .models import User,Video,Transcript,ConvertedVideo
import wave
import sys
from pydub import utils, AudioSegment
import soundfile as sf
from django.contrib.auth import authenticate
from moviepy.editor import *
from pydub import AudioSegment 
import speech_recognition as sr
from gtts import gTTS
from googletrans import Translator, constants
import jwt
from datetime import datetime
from datetime import  timedelta
from django.conf import settings
KEYS = getattr(settings, "KEY_", None)
from transformers import AutoProcessor, BarkModel

from IPython.display import Audio
import scipy
import os
voices={
    'zh_male':'v2/zh_speaker_3',
    'zh_female':'v2/zh_speaker_7',
    'fr_male':'v2/fr_speaker_4',
    'fr_female':'v2/fr_speaker_1',
    'de_male':'v2/de_speaker_6',
    'de_female':'v2/de_speaker_3',
    'hi_female':'v2/hi_speaker_3',
    'hi_male':'v2/hi_speaker_7',
    'it_male':'v2/it_speaker_4',
    'it_female':'v2/it_speaker_9',
    'ja_male':'v2/ja_speaker_2',
    'ja_female':'v2/ja_speaker_0',
    'ko_male':'v2/ko_speaker_1',
    'ko_female':'v2/ko_speaker_0',
    'pl_male':'v2/pl_speaker_8',
    'pl_female':'v2/pl_speaker_4',
    'ru_male':'v2/ru_speaker_4',
    'ru_female':'v2/ru_speaker_6',
    'es_male':'v2/es_speaker_0',
    'es_female':'v2/es_speaker_9',
    'tr_male':'v2/tr_speaker_1',
    'tr_female':'v2/tr_speaker_4'
}


def video_to_audio(input_path):
    clip = VideoFileClip(input_path) 
    clip.audio.write_audiofile(r"chunk0.mp3")
def audio_to_audio(lang,song,voice):
    print('song',song)
    print("Hello",lang)
    arr=[i for i in range(10000,len(song),10000)]
    arr.insert(0,0)
    if len(song)>arr[-1]:
        arr.append(arr[-1]+len(song)-arr[-1])
        translator = Translator()
        recognizer = sr.Recognizer()
    o=''
    for i in range(0,len(arr)-1):
            a=song[arr[i]:arr[i+1]]
            print(arr[i])
            a.export("new.mp3", format="mp3") 
            sound = AudioSegment.from_mp3("new.mp3")
            sound.export(f'new{i}.wav', format="wav") 
  
            AUDIO_FILE = f"new{i}.wav"
            
            try:
                r = sr.Recognizer()
                with sr.AudioFile(AUDIO_FILE) as source:
                    audio = r.record(source)
                    text=r.recognize_google(audio)
                    print(text)
                    text=translator.translate(text,dest=lang)
                    print(text.text)
                    print('Hey')
                    o+=str(text.text)
                    voice_preset = voices.get(str(lang)+'_'+str(voice).lower())
                    print(voice_preset)
                    processor = AutoProcessor.from_pretrained("suno/bark")
                    model = BarkModel.from_pretrained("suno/bark")
                    inputs = processor(text.text, voice_preset=voice_preset)
                    audio_array = model.generate(**inputs)
                    audio_array = audio_array.cpu().numpy().squeeze()
                    sample_rate = model.generation_config.sample_rate
                    Audio(audio_array, rate=sample_rate)
                    sample_rate = model.generation_config.sample_rate
                    scipy.io.wavfile.write("audio{i}.wav", rate=sample_rate, data=audio_array)
                    if i==0:
                        scipy.io.wavfile.write("final_output.wav", rate=sample_rate, data=audio_array)
                    else:
                        a=AudioSegment.from_file('final_output.wav')
                        b=AudioSegment.from_file(f'audio{i}.wav')
                        a=a.append(b,crossfade=100)
                        a.export('final_output.wav',format='wav')
            except:
                pass
    return o
                


def audio_to_video(inp,output_path,vd_name,obj,type,o):
    video_clip = VideoFileClip(inp)
    audio_clip = AudioFileClip("final_output.wav")
    final_clip = video_clip.set_audio(audio_clip)
    print(output_path)
    final_clip.write_videofile(output_path)
    c_id=ConvertedVideo.objects.create(video_id=obj,type=type,videofile=vd_name)
    Transcript.objects.create(c_id=c_id,video_id=obj,script=o)

    
    

def start(inp_path,lang,out_path,vd_name,obj,type,output_type,voice): 
    print(inp_path,lang,out_path)  
    video_to_audio(inp_path)
    print('Hello')
    audio = AudioSegment.from_file(os.path.join(os.getcwd(),'chunk0.mp3'))
    print("Hey")
    o=audio_to_audio(lang,audio,voice)
    audio_to_video(inp_path,out_path,vd_name,obj,type,o)



# Create your views here.
def home(request):
    if request.session.has_key('email')  and request.session.get('role') == 'admin'  and request.session.has_key('token'):  
        try:
           
            d = jwt.decode(request.session.get('token'), key=KEYS, algorithms=['HS256'])
            if d.get('email')!=request.session.get('email'):
                return redirect('../../../')
        except:
            try:
                del request.session['email']          
            except:
                pass
            try:
                del request.session['role']       
            except:
                pass
            try:
                del request.session['token']    
            except:
                pass
            return redirect('../../../login')
    else:
        return redirect('../../login')
    if request.method=='POST':
        if 'submit' in request.POST:
            vd=request.FILES.get('video')
            type=request.POST.get('type')
            voice=request.POST.get('voice')
            hi=request.POST.get('hi')
            de=request.POST.get('de')
            es=request.POST.get('es')
            fr=request.POST.get('fr')
            it=request.POST.get('it')
            ja=request.POST.get('ja')
            ko=request.POST.get('ko')
            pl=request.POST.get('pl')
            ru=request.POST.get('ru')
            tk=request.POST.get('tk')
            zh=request.POST.get('zh')
            
            langs=[hi,de,es,fr,it,ja,ko,pl,ru,tk,zh]
            langs=[i for i in langs if i is not None]
            fl=FileSystemStorage()
            fl.save(vd.name,vd)
            obj=Video.objects.create(videofile=vd)
            for i in langs:
                start(os.path.join(os.getcwd(),'media',str(vd)),i,os.path.join(os.getcwd(),f'media/{i}',str(i)+str(vd)),os.path.join(i,str(i)+str(vd)),obj,i,type,voice)

            
            return redirect(f'../../download/{obj.id}')
    return render(request,'index.html')

def download(request,pk=None):
    if request.session.has_key('email')  and request.session.get('role') == 'admin'  and request.session.has_key('token'):  
        try:
            d = jwt.decode(request.session.get('token'), key=KEYS, algorithms=['HS256'])
            if d.get('email')!=request.session.get('email'):
                return redirect('../../../')
        except:
            try:
                del request.session['email']          
            except:
                pass
            try:
                del request.session['role']       
            except:
                pass
            try:
                del request.session['token']    
            except:
                pass
            return redirect('../../../login')
    else:
        return redirect('../../login')
    if pk is not None:
        data=ConvertedVideo.objects.filter(video_id=pk)
        return render(request,'index.html',{'data':data})
    else:
        return redirect('../../../')
    
def login(request):
        message=request.session.get('message')
        message1=request.session.get('message1')
        try:
            del request.session['message']
        except:
            pass
        try:
            del request.session['message1']
        except:
            pass
        if request.method=='POST': 
            em=request.POST.get('email')
            ps=request.POST.get('password')
            print(em)
            print(ps)
            try:
                username=User.objects.get(email=em).username
            except:
                message1='Incorrect Email Address'
                request.session['message1']=message1
                return redirect('../../../login')
            usr=authenticate(username=username,password=ps)
            print(usr)
            if usr is not None:
                if usr.verified_at=='True' and usr.status=='1':     
                        request.session['email']=em
                        request.session['role']=usr.role    
                        usr= User.objects.get(email=em) 
                        payload_ = {'email': em,'exp': datetime.utcnow() + timedelta(days=1)}
                        token = jwt.encode(payload=payload_,
                                   key=KEYS
                                   )
                        request.session['token']=token            
                        ip=request.META.get('HTTP_X_FORWARDED_FOR')
                        if ip:
                            ip=ip.split(',')[0]
                        else:
                            ip=ip = request.META.get('REMOTE_ADDR')

                        return redirect('../../../')
                else:
                    message1='Email or Password Incorrect'
                    request.session['message1']=message1
                    return redirect('../../../login')
            else:
                message1='Email or Password Incorrect'
                request.session['message1']=message1
                return redirect('../../../login')
        return render(request,'login.html',{'message':message,'message1':message1})


def logout(request):
    try:
        del request.session['email']
    except:
        pass
    try:
        del request.session['role']
    except:
        pass
    try:
        del request.session['token']
    except:
        pass
    return redirect('../../../login')
