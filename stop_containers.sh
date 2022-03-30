docker ps -a|grep $1 |awk '{print $NF;}'|xargs -i docker stop {}
