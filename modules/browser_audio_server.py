from fastapi import FastAPI, WebSocket
import numpy as np

class BrowserAudioServer:
    def __init__(self, speech_recognizer, on_text_callback):
        self.app = FastAPI()
        self.speech_recognizer = speech_recognizer
        self.on_text_callback = on_text_callback

        @self.app.websocket("/browser-audio")
        async def browser_audio(ws: WebSocket):
            await ws.accept()
            print("[INFO] Browser audio connected")

            while True:
                data = await ws.receive_bytes()
                audio = np.frombuffer(data, dtype=np.float32)

                result = self.speech_recognizer.add_browser_audio(audio)

                if result and result.get("text"):
                    self.on_text_callback(result)
