FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04

LABEL authors="JSK Robotics Laboratory, The University of Tokyo"

ADD . /app

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip

RUN python3 -m pip install -r requirements.txt

ENV PATH=/usr/local/cuda/bin:${PATH}
ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:${LD_LIBRARY_PATH}

ENTRYPOINT ["python3", "voice_filter_service.py"]