# Install
```
brew install -y python-opengl ffmpeg
brew install -y --cask xquartz
```

# Running
```
docker build . -t hugginface-train-1
docker run -it hugginface-train-1 /bin/bash
```