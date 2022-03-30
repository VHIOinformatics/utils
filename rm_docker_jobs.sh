docker ps -a|grep "Exited" |awk '{print $NF;}'|xargs -i docker rm {}
