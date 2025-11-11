sudo docker run -d \
  --name tony_agents \
  --restart always \
  --device /dev/snd \
  --device /dev/video0 \
  --gpus all \
  -p 5050:5050 -p 5051:5051 -p 8000:8000 \
  -v /mnt/ssd/jetson_data:/app/data \
  jetson-ai-agents
