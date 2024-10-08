# Choose Amazon Linux 2
# Reference:
# https://gist.github.com/npearce/6f3c7826c7499587f00957fee62f8ee9
# ######
# On EC2
# ######

sudo yum update -y

# Install docker
sudo amazon-linux-extras install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user
docker --version

# Install docker-compose
sudo curl \
  -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) \
  -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
# Make an alias
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
which docker-compose
docker-compose --version

# Create a folder for the destination
mkdir downloads
cd downloads/

################
# On dev machine
################

# Replace with EC2 IP
scp \
  -i aws/telegram-relationship-bot.pem \
  -r docker/ src/ .dockerignore ec2-user@{ec2_ip}:/home/ec2-user/downloads

# Encrypt the private key to put on GitHub
base64 \
  -i aws/telegram-relationship-bot.pem \
  -o aws/key.b64

cat aws/key.b64 | pbcopy

# ######
# On EC2
# ######
sudo docker-compose -f docker/prod/docker-compose.yaml up --build
