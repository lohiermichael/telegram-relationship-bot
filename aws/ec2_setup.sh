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

# Install git
sudo yum install git -y
git --version
git config --global user.name "Firstname Lastname"
git config --global user.email "email@example.com"


ssh-keygen -t rsa -b 4096 -C "email@example.com"

cat ~/.ssh/id_rsa.pub
# Copy and store it in GitHub:  Settings > SSH and GPG keys > New SSH key

# Generate Personal Access Token with ecessary scopes (e.g., repo
# for full control of private repositories).
# Clone the repository
git clone https://{your-token}@github.com/lohiermichael/telegram-relationship-bot.git




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

# Connect with ssh to the instance
ssh -i aws/telegram-relationship-bot.pem ec2-user@{ec2_ip}


# ######
# On EC2
# ######
sudo docker-compose -f docker/prod/docker-compose.yaml up --build
