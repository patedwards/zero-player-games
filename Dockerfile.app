FROM 742309522247.dkr.ecr.us-east-2.amazonaws.com/corvusio-app:latest

COPY src /app/src
COPY setup.py /app/setup.py
COPY requirements.txt /app/requirements.txt
COPY training /app/training

RUN pip install -e .

# Set the entrypoint to Python
ENTRYPOINT ["python3.10"]
