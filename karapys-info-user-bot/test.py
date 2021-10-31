from os import path as p
s = 'voice/file_9.wav'
s = p.join('files', 'voice', 'wav', p.basename(s))
print(s)