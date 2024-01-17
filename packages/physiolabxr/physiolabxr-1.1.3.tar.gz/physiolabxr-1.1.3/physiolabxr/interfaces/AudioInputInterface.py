import time
import numpy as np
import pyaudio

from physiolabxr.interfaces.DeviceInterface.DeviceInterface import DeviceInterface
from physiolabxr.presets.PresetEnums import PresetType
from physiolabxr.presets.presets_utils import get_audio_device_index, get_stream_num_channels, \
    get_audio_device_data_type, get_audio_device_frames_per_buffer, get_audio_device_sampling_rate, \
    get_stream_nominal_sampling_rate
from physiolabxr.utils.time_utils import get_clock_time


class AudioInputInterface(DeviceInterface):

    def __init__(self,
                 _device_name,
                 _audio_device_index,
                 _audio_device_channel,
                 _device_type,
                 audio_device_data_format=pyaudio.paInt16,
                 audio_device_frames_per_buffer=128,
                 audio_device_sampling_rate=4000,
                 device_nominal_sampling_rate=4000):
        super(AudioInputInterface, self).__init__(_device_name=_device_name,
                                                  _device_type=_device_type,
                                                  device_nominal_sampling_rate=device_nominal_sampling_rate)

        self._audio_device_index = _audio_device_index
        self._audio_device_channel = _audio_device_channel
        self.audio_device_data_format = audio_device_data_format
        self.audio_device_frames_per_buffer = audio_device_frames_per_buffer
        self.audio_device_sampling_rate = audio_device_sampling_rate

        # self.audio_device_index = audio_device_index
        # self.frames_per_buffer = frames_per_buffer
        # self.format = data_format
        # self.channels = channels
        #
        self.frame_duration = 1 / self.audio_device_sampling_rate

        self.audio = None
        self.stream = None

    def start_stream(self):
        self.audio = pyaudio.PyAudio()

        # open stream
        self.stream = self.audio.open(format=self.audio_device_data_format,
                                      channels=self._audio_device_channel,
                                      rate=self.audio_device_sampling_rate,
                                      frames_per_buffer=self.audio_device_frames_per_buffer,
                                      input=True,
                                      input_device_index=self._audio_device_index)
        # start stream
        self.stream.start_stream()

    def process_frames(self):
        # read all data from the buffer
        # try:
        frames = self.stream.read(self.stream.get_read_available(), exception_on_overflow=False)
        # except IOError as e:
        #     if e[1] != pyaudio.paInputOverflowed:
        #         raise
        #     data = b'\x00' * self.frames_per_buffer
        #     print("Buffer Error")

        current_time = time.time()

        samples = len(frames) // (
                    self._audio_device_channel * self.audio.get_sample_size(self.audio_device_data_format))
        timestamps = np.array([current_time - (samples - i) * self.frame_duration for i in range(samples)])
        timestamps = timestamps - timestamps[-1] + get_clock_time() if len(frames) > 0 else np.array([])

        # byte frames to numpy
        frames = np.frombuffer(frames, dtype=np.int16)

        # frames to channel frames
        frames = np.array_split(frames, self._audio_device_channel)

        return np.array(frames), timestamps

    def stop_stream(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()

    def is_stream_available(self):

        return True
        # return True


def create_audio_input_interface(stream_name):

    _audio_device_index = get_audio_device_index(stream_name)
    _audio_device_channel = get_stream_num_channels(stream_name)
    _device_type = PresetType.AUDIO
    audio_device_data_format = get_audio_device_data_type(stream_name)
    audio_device_frames_per_buffer = get_audio_device_frames_per_buffer(stream_name)
    audio_device_sampling_rate = get_audio_device_sampling_rate(stream_name)
    device_nominal_sampling_rate = get_stream_nominal_sampling_rate(stream_name)

    audio_input_device_interface = AudioInputInterface(
        stream_name,
        _audio_device_index,
        _audio_device_channel,
        _device_type,
        audio_device_data_format.value,
        audio_device_frames_per_buffer,
        audio_device_sampling_rate,
        device_nominal_sampling_rate
    )
    return audio_input_device_interface
