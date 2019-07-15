FROM homeassistant/home-assistant
  
RUN apt-get update && apt-get install -y vlc ffmpeg

CMD [ "python", "-m", "homeassistant", "--config", "/config" ]
