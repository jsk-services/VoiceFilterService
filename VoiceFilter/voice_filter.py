import datetime
import io
from io import BytesIO
from typing import BinaryIO

import numpy as np
import librosa
import soundfile as sf
import onnxruntime as ort
from VoiceFilter.audio_utils import Audio

# Audio
SAMPLING_RATE = 16000

class VoiceFilter:
    def __init__(self):
        self._filter = ort.InferenceSession('./VoiceFilter/filter.onnx',
                                            providers=['CUDAExecutionProvider'])
        self._filter_inputs = self._filter.get_inputs()
        print(self._filter.get_providers())
        self._embedder = ort.InferenceSession('./VoiceFilter/embedder.onnx',
                                              providers=['CUDAExecutionProvider'])
        self._embedder_inputs = self._embedder.get_inputs()
        print(self._embedder.get_providers())
        self._audio = Audio()
        pass

    @staticmethod
    def _prepare_wave(data: BinaryIO, sample_rate: int = None):
        # prepare input data
        wav, source_sr = librosa.load(data, sr=sample_rate)
        # Resample the wav if needed
        if source_sr is not None and source_sr != SAMPLING_RATE:
            wav = librosa.resample(wav, orig_sr=source_sr, target_sr=SAMPLING_RATE)
        return wav

    def embed(self, audio_data: BinaryIO, sample_rate: int = None) -> np.ndarray:
        reference_wave = VoiceFilter._prepare_wave(audio_data, sample_rate)
        reference_mel = self._audio.get_mel(reference_wave)
        reference_vector = self._embedder.run(None, {
            self._embedder_inputs[0].name: reference_mel[:, :301]})
        return reference_vector[0]
    
    def filter(self, reference_vector, audio_data: BinaryIO, sample_rate: int = None) -> bytes:
        mixed_wave = VoiceFilter._prepare_wave(audio_data, sample_rate)
        # Get the magnitude spectrogram and phase.
        mag, phase = self._audio.wav2spec(mixed_wave)
        mag = np.expand_dims(mag, axis=0)
        reference_vector = np.expand_dims(reference_vector, axis=0).astype(np.float32)
        mask = self._filter.run(None, {
            self._filter_inputs[0].name: mag,
            self._filter_inputs[1].name: reference_vector
        })[0]
        # Apply mask to the magnitude spectrogram.
        est_mag = mag * mask
        est_wave = self._audio.spec2wav(est_mag[0], phase)
        # Write .wav into buffer.
        buffer = io.BytesIO()
        sf.write(buffer, est_wave, SAMPLING_RATE, 'PCM_24', format='WAV')
        buffer.seek(0)
        return buffer.read()