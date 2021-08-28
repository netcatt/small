import speech_recognition

import time

language = "pl-PL"
input_device_index = None
stop_listening = None


def _listener_callback(recognizer, audio):
    print("Processing audio")

    try:
        recognized_text = recognizer.recognize_google(audio, language=language)
        print(f"Recognized: {recognized_text}")
        with open("output.txt", "a", encoding="utf-8") as file:
            file.write(recognized_text + "\n")
            file.close()

    except speech_recognition.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except speech_recognition.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")


answer = input("Do you want to use default device (Y/n): ")
if answer.upper() == "N":
    for index, name in enumerate(speech_recognition.Microphone.list_microphone_names()):
        print(
            f'Microphone with name {name} found for `Microphone(device_index={index})'
        )

    input_device_index = int(input("Select you input device: "))
else:
    input_device_index = None

speech_recognizer = speech_recognition.Recognizer()
print("Initialized recogninzer")

microphone = speech_recognition.Microphone(device_index=input_device_index)
print("Initialized microphone")

stop_listening = speech_recognizer.listen_in_background(
    microphone, _listener_callback
)
print("Started listening")
while True:
    time.sleep(1)
