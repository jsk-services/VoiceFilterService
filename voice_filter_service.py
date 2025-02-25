import os
from concurrent import futures
from io import BytesIO

import grpc
import VoiceFilterService_pb2 as Messages
import VoiceFilterService_pb2_grpc as Services

from VoiceFilter.voice_filter import VoiceFilter


class VoiceFilterServer(Services.VoiceFilterServiceServicer):
    def __init__(self, model: VoiceFilter):
        self._model = model
        pass

    def Embed(self, request: Messages.EmbedRequest, context):
        return Messages.EmbedResponse(
            Embedding=self._model.embed(BytesIO(request.Audio), sample_rate=16000)
        )

    def Filter(self, request: Messages.FilterRequest, context):
        return Messages.FilterResponse(
            Audio=self._model.filter(
                request.Embedding,
                BytesIO(request.Audio),
                sample_rate=16000
            )
        )


if __name__ == "__main__":
    port = os.environ.get("PORT", 50000)
    token = os.environ.get("TOKEN", "")
    
    print("Preparing models...")

    filter_model = VoiceFilter()
    
    print("Preparing server...")

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Services.add_VoiceFilterServiceServicer_to_server(
        VoiceFilterServer(filter_model), server)

    print(f"Server address: [::]:{port}")

    server.add_insecure_port(f"[::]:{port}")
    server.start()
    server.wait_for_termination()
    pass