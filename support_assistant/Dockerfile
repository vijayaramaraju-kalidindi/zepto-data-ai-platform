FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install CPU-only PyTorch to avoid CUDA/NVIDIA packages.
RUN pip install --no-cache-dir \
    torch \
    --index-url https://download.pytorch.org/whl/cpu

COPY support_assistant/docker-requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY support_assistant /app/support_assistant

ENV PYTHONPATH=/app/support_assistant

EXPOSE 7860

CMD ["uvicorn", "support_assistant.api.main:app", "--host", "0.0.0.0", "--port", "7860"]