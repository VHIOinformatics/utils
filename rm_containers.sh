sudo docker ps -a|grep Exited |awk '{print ;}'|xargs -i sudo docker rm {}
