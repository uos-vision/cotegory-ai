FROM python:3.10

ARG AUTO_ENCODER_MODEL_ID
ARG EASE_MODEL_ID

ENV AUTO_ENCODER_MODEL_ID=${AUTO_ENCODER_MODEL_ID}
ENV EASE_MODEL_ID=${EASE_MODEL_ID}

WORKDIR /app

COPY requirements.txt .
RUN pip freeze > installed_packages.txt

RUN pip install --no-cache-dir -r requirements.txt --requirement installed_packages.txt
RUN pip3 install torch torchvision torchaudio --requirement installed_packages.txt

RUN apt-get update && apt-get install -y curl

RUN mkdir -p model/saved/auto-encoder \
    && if [ ! -f "model/saved/auto-encoder/auto_encoder_model.pt" ]; then \
        curl -o model/saved/auto-encoder/auto_encoder_model.pt "https://drive.google.com/uc?export=download&id=${AUTO_ENCODER_MODEL_ID}"; \
    fi

RUN mkdir -p model/saved/ease \
    && if [ ! -f "model/saved/ease/ease_model.npz" ]; then \
        curl -o model/saved/ease/ease_model.npz "https://drive.google.com/uc?export=download&id=${EASE_MODEL_ID}"; \
    fi

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=8000", "--reload"]
