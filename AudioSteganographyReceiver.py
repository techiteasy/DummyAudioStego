import socket
from Client.decodeAudioSteganography import decodeWavFile
s = socket.socket()
host = socket.gethostname()
port = 60000

s.connect((host, port))


with open('received_file.wav', 'wb') as f:
    print('file opened')
    while True:
        print('receiving data...')
        data = s.recv(1024)
        print('data', data)
        if not data:
            break
        f.write(data)

f.close()
print('Successfully get the file')
s.close()
if(decodeWavFile()):
    print('Encoded Wav File')
print('connection closed')




