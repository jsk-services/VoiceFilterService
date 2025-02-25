import datetime
import os
import grpc
import soundfile

import VoiceFilterService_pb2 as Messages
import VoiceFilterService_pb2_grpc as Services


def read_audio(path: str):
    with open(path, "rb") as file:
        return file.read()

if __name__ == "__main__":

    with (grpc.insecure_channel('dlbox13:50002') as channel):
        stub = Services.VoiceFilterServiceStub(channel)
        
        
        embedding = stub.Embed(Messages.EmbedRequest(Audio=read_audio("ref-voice.wav"))
                               ).Embedding

        for index in range(10):

            timestamp = datetime.datetime.now()
            filtered = stub.Filter(Messages.FilterRequest(
                Audio=read_audio("mixed.wav"),
                Embedding=embedding
            )).Audio
            print(f"Time taken: {(datetime.datetime.now() - timestamp).microseconds / 1000} ms")
        
        pass