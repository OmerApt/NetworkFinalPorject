# Will contain the class for a Quic Packet
import pickle
from abc import ABC, abstractmethod


class QuicHeader:
    # flags: bytes
    # "flags for the header"

    packet_number: int
    "The packet number"

    destination_cid: bytes
    "The destination connection ID."

    header_form: bool
    "if the header is a short header true else is a long header"

    def __init__(self, packet_number, destination_cid, header_form):
        # self.flags = 0
        self.packet_number = packet_number
        self.destination_cid = destination_cid
        self.header_form = header_form

    def __str__(self):
        return f"destination_cid: {self.destination_cid}, packet_number: {self.packet_number}"

    def get_packet_number(self):
        return self.packet_number

    # serialize header
    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    # deserialize header
    def __setstate__(self, state):
        self.__dict__.update(state)

    @staticmethod
    def packet_number_generate():
        return 0

    class QuicFrame(ABC):
        def __init__(self, frame_type):
            self.frame_type = frame_type

            # deserialize header

        def __getstate__(self):
            state = self.__dict__.copy()
            return state

        # deserialize header
        def __setstate__(self, state):
            self.__dict__.update(state)

        @abstractmethod
        def __str__(self):
            pass

    # a Stream frame containing data
    class QuicFrameStream(QuicFrame):
        def __str__(self):
            pass

        def __init__(self, frame_type, frame_offset, frame_length, stream_data):
            super().__init__(frame_type)
            self.stream_id = 0
            self.frame_offset = frame_offset
            self.length = frame_length
            self.data = stream_data

    # an ack frame without field ACK Delay
    class QuicFrameAcks(QuicFrame):
        def __init__(self, frame_type, largest_ack, range_count, ack_ranges):
            super().__init__(frame_type)
            self.largest_ack = largest_ack
            self.range_count = range_count
            self.ack_ranges = ack_ranges  # might need change

        def __str__(self):
            return f"frame_type: @{self.frame_type} | largest_ack: {self.largest_ack} | range_count: {self.range_count}"

    class QuicPacket():
        def __init__(self, packet_header, packet_frames):
            self.header = packet_header
            self.frames = packet_frames

        def __getstate__(self):
            state = self.__dict__.copy()
            state["header"] = pickle.dumps(state["header"])
            state["frames"] = [pickle.dumps(frame) for frame in state["frames"]]
            return state

        def __setstate__(self, state):
            self.__dict__.update(state)
            self.header = pickle.loads(state["header"])
            self.frames = [pickle.loads(frame) for frame in state["frames"]]

        def __str__(self):
            return f"header: {self.header}\n frames: {self.frames}\n"
