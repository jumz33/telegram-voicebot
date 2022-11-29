from io import BytesIO
from pydub import AudioSegment
from speech_recognition import Recognizer, AudioFile, UnknownValueError
from objects import Voice, VideoNote


class TextRecognizer:
    def __init__(self, text_language="en-US"):
        self._text_language = text_language
        self._recognizer = Recognizer()

    def in_voice(self, voice: Voice):
        ogg = BytesIO(voice.ogg_bytes)
        wav = self._ogg_to_wav(ogg)
        return self._recognize_from_wav(wav)

    def in_video_note(self, video_note: VideoNote):
        ...

    @staticmethod
    def _ogg_to_wav(ogg: BytesIO) -> BytesIO:
        audio = AudioSegment.from_ogg(ogg)
        return audio.export(BytesIO(), format="wav")

    def _recognize_from_wav(self, wav: BytesIO):
        audio_data = self._get_audio_data_from_wav(wav)
        return self._try_to_recognize_from_audio_data(audio_data)

    def _get_audio_data_from_wav(self, wav):
        with AudioFile(wav) as source:
            self._recognizer.adjust_for_ambient_noise(source)
            return self._recognizer.record(source)

    def _try_to_recognize_from_audio_data(self, audio_data):
        try:
            return self._recognizer.recognize_google(
                audio_data=audio_data,
                language=self._text_language
            )
        except UnknownValueError:
            raise TextRecognizerException("no text found")


class TextRecognizerException(Exception):
    pass
