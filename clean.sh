#!/bin/bash

remove_container() {
    docker stop $(docker container ps -f since=broccoli -qa)
    docker rm $(docker container ps -f since=broccoli -qa)
}

remove_volume_and_image() {
    remove_container
    docker volume rm $(docker volume ls -f name=broccoli -q)
    docker rmi -f $(docker images broccoli -qa)
}

remove_volume_and_image