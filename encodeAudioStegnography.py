import wave
import os
import math


def generateSteganography():
    audio_file = wave.open('inputAudio.wav', 'r')
    hidden_file = open('data.txt', 'r')

    file_size = os.path.getsize('data.txt')

    spreading_factor = audio_file.getnframes() // file_size

    print("Encoding File Size: " + str(file_size))
    print("No of Frames in Audio Input: " + str(audio_file.getnframes()))

    init_buff = []

    # Minimum no of frames of audio signal is 60 to be able to encode a message
    if spreading_factor >= 60:
        spread = math.floor(spreading_factor / 2)
        init_buff = audio_file.readframes(-1)
        init_buff = [item for item in init_buff]
        audio_file.setpos(0)
        mod_buff = []

        while True:
            dest_file = wave.open('output.wav', 'w')
            dest_file.setnchannels(audio_file.getnchannels())
            dest_file.setsampwidth(audio_file.getsampwidth())
            dest_file.setframerate(audio_file.getframerate())
            dest_file.setnframes(audio_file.getnframes())

            user_choice = "y"
            if (user_choice.lower() == "yes" or user_choice.lower() == "y"):
                # Read n frames from the audio signal
                buf = bytearray(audio_file.readframes(spreading_factor))
                buflen = len(buf)
                print(buflen)
                while (len(buf) > 0):
                    data = hidden_file.read(1)

                    if data:
                        data = ord(data)
                        # print(data)
                        for i in range(8):
                            # print(str(data) + "::" + str(i))
                            bit = data >> i
                            # print (bit)
                            f_byte = int(i * spread)  # + random.randint(0,spread - 1))
                            # print("F_BYTE: " + str(f_byte))

                            if f_byte % 2 == 1:
                                f_byte -= 1

                            if (f_byte >= buflen):
                                f_byte = int(f_byte / buflen)

                            if buf[f_byte] % 2 == 0 and bit % 2 == 1:
                                buf[f_byte] += 1
                            elif buf[f_byte] % 2 == 1 and bit % 2 == 0:
                                buf[f_byte] -= 1
                    try:

                        mod_buff.extend(buf)
                        dest_file.writeframes(buf)
                        buf = bytearray(audio_file.readframes(spreading_factor))

                    except wave.Error as e:
                        print(str(e))

                print("The Spreading Factor is ", spreading_factor * 4)
                dest_file.close()
                break
            elif user_choice.lower() == "no" or user_choice.lower() == "n":
                print("Proceed to exit")
                break
            else:
                print("Please enter yes or no")
        print("DONE")

    else:
        print("Is NOT enough to continue, you need a bigger wav file")

    hidden_file.close()
    audio_file.close()
    return True


if __name__ == '__main__':
    generateSteganography()
