"""
Speech Recognition Module - Convert audio to text using Whisper
"""
import whisper
import numpy as np
import torch


class SpeechRecognizer:
    def __init__(self, model_size='tiny', language=None):
        """
        Initialize speech recognizer with Whisper
        
        Args:
            model_size: Whisper model size ('tiny', 'base', 'small', 'medium', 'large')
                       tiny: fastest, least accurate (~75MB)
                       base: good balance (~150MB)
                       small: better accuracy (~500MB)
            language: Source language code (None for auto-detect)
        """
        self.model_size = model_size
        self.language = language
        self.model = None
        self.sample_rate = 16000  # Whisper expects 16kHz
        
    def load_model(self):
        """Load the Whisper model"""
        try:
            print(f"[INFO] Loading Whisper model '{self.model_size}'...")
            print("[INFO] This may take a minute for first-time download...")
            
            # Check if CUDA is available
            device = "cuda" if torch.cuda.is_available() else "cpu"
            print(f"[INFO] Using device: {device}")
            
            self.model = whisper.load_model(self.model_size, device=device)
            print(f"[OK] Whisper model loaded successfully")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to load Whisper model: {e}")
            return False
    
    def transcribe_audio(self, audio_data):
        """
        Transcribe audio to text
        
        Args:
            audio_data: numpy array of audio samples (16kHz)
            
        Returns:
            dict with 'text' and 'language' keys, or None on error
        """
        if self.model is None:
            print("[ERROR] Model not loaded. Call load_model() first")
            return None
        
        try:
            # Ensure audio is the right format
            if isinstance(audio_data, list):
                audio_data = np.array(audio_data)
            
            # Convert to float32 and normalize
            audio_data = audio_data.astype(np.float32)
            
            # Whisper expects audio in range [-1, 1]
            if audio_data.max() > 1.0 or audio_data.min() < -1.0:
                audio_data = audio_data / np.abs(audio_data).max()
            
            # Transcribe
            options = {
                'language': self.language,
                'task': 'transcribe',
                'fp16': False  # Use fp32 for CPU
            }
            
            result = self.model.transcribe(audio_data, **options)
            
            return {
                'text': result['text'].strip(),
                'language': result.get('language', 'unknown')
            }
            
        except Exception as e:
            print(f"[ERROR] Transcription failed: {e}")
            return None
    
    def transcribe_audio_stream(self, audio_chunks, min_duration=2.0):
        """
        Transcribe from continuous audio stream
        Accumulates chunks until minimum duration is reached
        
        Args:
            audio_chunks: List of numpy arrays
            min_duration: Minimum audio duration in seconds before transcribing
            
        Returns:
            Transcription result or None if not enough audio yet
        """
        # Concatenate all chunks
        if not audio_chunks:
            return None
        
        audio_data = np.concatenate(audio_chunks)
        
        # Check if we have enough audio
        duration = len(audio_data) / self.sample_rate
        if duration < min_duration:
            return None
        
        # Transcribe
        return self.transcribe_audio(audio_data)


class RealtimeSpeechRecognizer:
    """
    Real-time speech recognition with buffer management
    """
    def __init__(self, model_size='tiny', language=None):
        self.recognizer = SpeechRecognizer(model_size, language)
        self.audio_buffer = []
        self.buffer_duration = 0
        self.min_buffer_duration = 2.0  # Transcribe every 2 seconds
        self.max_buffer_duration = 5.0  # Maximum 5 seconds buffer
        self.sample_rate = 16000
        
    def load_model(self):
        """Load the Whisper model"""
        return self.recognizer.load_model()
    
    def add_audio(self, audio_chunk):
        """
        Add audio chunk to buffer
        
        Args:
            audio_chunk: numpy array of audio samples
            
        Returns:
            Transcription result if buffer is ready, None otherwise
        """
        # Flatten the audio chunk if it's 2D (stereo)
        if audio_chunk.ndim > 1:
            audio_chunk = audio_chunk.flatten()
        
        # Add to buffer
        self.audio_buffer.append(audio_chunk)
        chunk_duration = len(audio_chunk) / self.sample_rate
        self.buffer_duration += chunk_duration
        
        # Check if we have too much audio (prevent memory overflow)
        if self.buffer_duration >= self.max_buffer_duration:
            print(f"[WARN] Buffer overflow, clearing old audio (buffer was {self.buffer_duration:.1f}s)")
            # Keep only the most recent chunks
            self.audio_buffer = self.audio_buffer[-5:]  # Keep last 5 chunks
            self.buffer_duration = sum(len(chunk) for chunk in self.audio_buffer) / self.sample_rate
        
        # Check if we have enough audio to transcribe
        if self.buffer_duration >= self.min_buffer_duration:
            # Transcribe accumulated audio
            result = self._transcribe_buffer()
            
            # Clear buffer after transcription
            self.clear_buffer()
            
            return result
        
        return None
    
    def _transcribe_buffer(self):
        """Transcribe the current buffer"""
        if not self.audio_buffer:
            return None
        
        try:
            # Concatenate all chunks
            audio_data = np.concatenate(self.audio_buffer)
            
            # Limit audio length to prevent memory issues
            max_samples = self.sample_rate * self.max_buffer_duration
            if len(audio_data) > max_samples:
                print(f"[WARN] Audio too long ({len(audio_data)} samples), trimming to {max_samples}")
                audio_data = audio_data[-max_samples:]  # Keep most recent
            
            # Transcribe
            return self.recognizer.transcribe_audio(audio_data)
        
        except Exception as e:
            print(f"[ERROR] Buffer transcription failed: {e}")
            return None
    
    def clear_buffer(self):
        """Clear the audio buffer"""
        self.audio_buffer = []
        self.buffer_duration = 0
