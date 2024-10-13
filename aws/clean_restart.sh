sudo docker-compose -f docker/prod/docker-compose.yaml down
rm src/data/data.json
cp src/data/data_template.json src/data/data.json
sudo docker-compose -f docker/prod/docker-compose.yaml up --build -d
tmux attach-session -t logs
