import pyaudio
import numpy as np
import time
import pydirectinput
import keyboard

# Define parameters for audio stream
chunk_size = 2048
sample_rate = 44100
rms_threshold = 35
x=0
durchschnitt=2
halth=int(durchschnitt)
all = [1,2]
# Define key mapping for kalimba keyse and two-part shortcuts

def find_nearest_value(my_dict, input_num):
    closest_key = None
    closest_diff = float('inf')
    
    for key in my_dict:
        diff = abs(key - input_num)
        if diff < closest_diff:
            closest_key = key
            closest_diff = diff
    #return my_dict[closest_key]
    return closest_key

c1=301
d1=345
e1=366
f1=431
g1=452
a1=495
b1=560
c2=603
d2=668
e2=754
f2=775
g2=904
a2=1012
b2=1120
c3=1206
d3=1335
e3=1486

start_time=0
wait_time=0.4

freqlist=[]
key_whole = {
c1,d1,e1,f1,g1,a1,c2,d2,e2,f2,g2,a2,b2,c3,d3,e3,b1
}

key_map = {
    c1: ('w', 'space'),
    e1: ('d', 'space'),
    d1: ('s', 'space'),
    f1: ('a', 'space'),
    g1: 'u',
    a1: 'down',
    b1: 'r',
    c2: ('m','',''),
    e2: ('o','',''),
    g2: ('l','',''),
    b2: ('n','',''),
    d2: 'k',
    f2: 'e',
    a2: 'right',
    c3: 'f',
    d3: 'w',
    e3: 'esc',

}

# Initialize PyAudio and audio stream
pa = pyaudio.PyAudio()
stream = pa.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=sample_rate,
    input=True,
    frames_per_buffer=chunk_size
)

while True:
    if keyboard.is_pressed("F2"):
        break
    
    # Read audio data and convert to numpy array
    audio_data = stream.read(chunk_size)
    audio_array = np.frombuffer(audio_data, dtype=np.int16)

    # Calculate root mean square (RMS) of audio signal
    rms = np.sqrt(np.mean(np.square(audio_array)))
    
    # Continue if RMS is below threshold
    if time.time() - start_time <wait_time:
        continue
    if rms < rms_threshold:
        continue 
    
    # Compute FFT and extract positive frequency components and corresponding frequencies
    fft_data = np.fft.fft(audio_array)
    positive_freq = np.abs(fft_data[:len(fft_data)//2])
    freqs = np.fft.fftfreq(len(fft_data), 1/sample_rate)[:len(fft_data)//2]
    
    # Find the dominant frequency and round it to the nearest integer
    idx = np.argmax(positive_freq)
    frequency = round(freqs[idx])
    
    if frequency <=280 or frequency >=1500:

        continue
    # Map the frequency to a corresponding key or key combination and press it
    #else:
    #    print("freqin: "+str(frequency))
    #    continue
    #print("freqin: " +str(int(frequency)))
    frequency= find_nearest_value(key_whole, frequency)

    #all[2]=all[1]
    all[1]=all[0]
    all[0]=frequency
    #==all[2]
    #if all[0]==all[1]:
    #    print("all:" +str(all))
    #else:
    #    continue
    #freqlist.append(frequency)
    #if len(freqlist) >durchschnitt:
     #   freqlist = sorted(freqlist)
     #   frequency = freqlist[halth]
    #    print(freqlist)
    #else:
    #    continue
    #print(frequency)
    # output: "ghello"

    #elif frequency == f1:
    #    pydirectinput.click(button='left')
    #    print('left click')
    #elif frequency == g2:
    #    pydirectinput.click(button='middle')
    #    print('middle click')
    #elif frequency == a1:
    #    pydirectinput.keyDown('shift')
    #    pydirectinput.click(button='left')
    #    pydirectinput.keyUp('shift')
    #    print('shift + left click') 

    try:
        key = key_map[frequency]

        if (isinstance(key,list)) and len(key)>2:
            pydirectinput.keyDown(key)
 
            pydirectinput.keyUp(key)
            print(key)
            print(2)

        if isinstance(key, str):
            pydirectinput.keyDown(key)
            pydirectinput.keyUp(key)
            print(key)
       
        else:
            pydirectinput.keyDown(key[0])
            pydirectinput.keyDown(key[1])
        
            pydirectinput.keyUp(key[1])
            pydirectinput.keyUp(key[0])
    except KeyError:
        pass
    start_time=time.time()
    #print(start_time)

    # Print the dominant frequency for debugging purposes
    print("freq:", frequency)
    freqlist=[]
    # Wait for a short time to avoid overloading the system
    #time.sleep(0.1)

