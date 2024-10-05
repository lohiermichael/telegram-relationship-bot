# On EC2
sudo yum update -y
sudo amazon-linux-extras install docker
sudo service docker start
sudo usermod -a -G docker ec2-user
mkdir downloads
cd downloads/

# On dev machine
scp -i telegram-relationship-bot.pem -r docker/ src/ ec2-user@15.188.11.88:/home/ec2-user/download

# On EC2
docker compose -f docker/prod/docker-compose.yaml up --build
sudo docker build -t telegram-relationship-bot:v1.0 -f docker/dev/Dockerfile .
sudo docker images
sudo docker run --env-file docker/dev/.env telegram-relationship-bot:v1.0
