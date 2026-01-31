"""
Audio Capture Module - Capture system audio for video translation
Uses WASAPI loopback to record what the user is hearing
"""
import sounddevice as sd
import numpy as np
import queue
import threading


class AudioCapture:
    def __init__(self, sample_rate=16000, channels=1):
        """
        Initialize audio capture
        
        Args:
            sample_rate: Sample rate in Hz (16000 is good for speech recognition)
            channels: Number of audio channels (1=mono, 2=stereo)
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.is_recording = False
        self.audio_queue = queue.Queue()
        self.stream = None
        
    def list_devices(self):
        """List all available audio devices"""
        print("\n=== Available Audio Devices ===")
        devices = sd.query_devices()
        for i, device in enumerate(devices):
            print(f"{i}: {device['name']}")
            print(f"   Max Input Channels: {device['max_input_channels']}")
            print(f"   Max Output Channels: {device['max_output_channels']}")
            print(f"   Default Sample Rate: {device['default_samplerate']}")
        return devices
    
    def get_loopback_device(self):
        """
        Find the best available audio input device
        Tries to find WASAPI loopback, then falls back to default input
        Returns device index or None
        """
        devices = sd.query_devices()
        
        # Try to find enabled loopback devices
        candidates = []
        
        for i, device in enumerate(devices):
            name = device['name'].lower()
            max_input = device['max_input_channels']
            
            # Check if device has input channels
            if max_input > 0:
                # Prioritize loopback devices
                if any(keyword in name for keyword in ['stereo mix', 'wave out', 'what u hear', 'loopback']):
                    candidates.append((i, device, 'loopback'))
                elif 'microphone' not in name:  # Also consider other non-microphone inputs
                    candidates.append((i, device, 'input'))
        
        # Try loopback devices first
        for idx, device, device_type in candidates:
            if device_type == 'loopback':
                try:
                    # Test if device can be opened
                    test_stream = sd.InputStream(
                        device=idx,
                        channels=1,
                        samplerate=self.sample_rate,
                        blocksize=1024
                    )
                    test_stream.close()
                    print(f"[OK] Using loopback device: {device['name']}")
                    return idx
                except Exception as e:
                    print(f"[WARN] Can't use {device['name']}: {e}")
                    continue
        
        # If no loopback works, try default input
        try:
            default_input = sd.default.device[0]
            if default_input is not None:
                device = devices[default_input]
                print(f"[INFO] Using default input device: {device['name']}")
                print("[INFO] Note: This will capture microphone, not system audio")
                return default_input
        except:
            pass
        
        print("[ERROR] No suitable audio device found")
        return None
    
    def audio_callback(self, indata, frames, time, status):
        """Callback function for audio stream"""
        if status:
            print(f"[WARN] Audio callback status: {status}")
        
        # Add audio data to queue
        self.audio_queue.put(indata.copy())
    
    def start_recording(self, callback=None):
        """
        Start recording system audio
        
        Args:
            callback: Optional callback function called with audio chunks
        """
        if self.is_recording:
            print("[WARN] Already recording")
            return False
        
        try:
            # Get loopback device
            device = self.get_loopback_device()
            
            # Start audio stream
            self.stream = sd.InputStream(
                device=device,
                channels=self.channels,
                samplerate=self.sample_rate,
                callback=self.audio_callback,
                blocksize=int(self.sample_rate * 0.5)  # 0.5 second chunks
            )
            
            self.stream.start()
            self.is_recording = True
            print(f"[OK] Started audio recording at {self.sample_rate}Hz")
            
            # Start processing thread if callback provided
            if callback:
                self.processing_thread = threading.Thread(
                    target=self._process_audio,
                    args=(callback,),
                    daemon=True
                )
                self.processing_thread.start()
            
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to start audio recording: {e}")
            return False
    
    def _process_audio(self, callback):
        """Process audio chunks from queue"""
        while self.is_recording:
            try:
                # Get audio chunk from queue (with timeout)
                audio_chunk = self.audio_queue.get(timeout=1.0)
                
                # Convert to mono if stereo
                if audio_chunk.shape[1] > 1:
                    audio_chunk = np.mean(audio_chunk, axis=1)
                
                # Call the callback with audio data
                callback(audio_chunk)
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"[ERROR] Audio processing error: {e}")
    
    def stop_recording(self):
        """Stop recording audio"""
        if not self.is_recording:
            return
        
        self.is_recording = False
        
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        
        # Clear the queue
        while not self.audio_queue.empty():
            try:
                self.audio_queue.get_nowait()
            except queue.Empty:
                break
        
        print("[OK] Stopped audio recording")
    
    def get_audio_chunk(self, timeout=1.0):
        """
        Get the next audio chunk from the queue
        
        Args:
            timeout: Timeout in seconds
            
        Returns:
            numpy array of audio data or None
        """
        try:
            return self.audio_queue.get(timeout=timeout)
        except queue.Empty:
            return None
