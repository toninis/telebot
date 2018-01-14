# telebot
Remote command execution via telegram bot

# token passthrough
export TELEBOT='your-token'

# Build as a docker
docker build --rm -t telebot:1.0.0 .

# Run as a docker
docker run -d --name telebot telebot:1.0.0
