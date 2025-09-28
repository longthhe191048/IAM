# lab 07: Docker Containers for Malware Analysis
<!-- TOC start (generated with https://github.com/derlin/bitdowntoc) -->

- [lab 07: Docker Containers for Malware Analysis](#lab-07-docker-containers-for-malware-analysis)
- [Objective](#objective)
- [Requirement](#requirement)
- [Pre-lab knowledge](#pre-lab-knowledge)
   * [Comparism ](#comparism)
      + [Virtual machine](#virtual-machine)
      + [Container - docker ](#container---docker)
   * [lab walkthrough](#lab-walkthrough)
      + [Installing docker and testing](#installing-docker-and-testing)
      + [Docker vs docker-compose](#docker-vs-docker-compose)
         - [Docker](#docker)
      + [Docker compose](#docker-compose)
   * [Installing REMnux docker container](#installing-remnux-docker-container)
   * [Reference](#reference)

<!-- TOC end -->
# Objective
* How to install docker
* Install REMnux docker container

# Requirement
* any linux virtual machine

# Pre-lab knowledge
* Docker is an open platform for developing, shipping, and running applications.
* Seperate infrastructure -> create a container (enviroment) for application
* Isolated enviroment
* Lightweight

## Comparism 
### Virtual machine
<img width="2240" height="1260" alt="image" src="https://github.com/user-attachments/assets/c0957a81-e555-4772-bd54-caa723ba1346" />

* Virtualize full Operating system kernel
* Compatible with all operating system due to independennt from the host machine
* large
* Start an instance require a few minutes
* more secure

### Container - docker 
<img width="2240" height="1260" alt="image" src="https://github.com/user-attachments/assets/ff50f6b5-e13e-4265-bc72-96df1d480ad3" />

* Virtualize only application layer, run on top of host operating system
* Compatible with any linux distribution
* lightweight
* near-native performance - start in a few second
* less secure

<img width="2240" height="1260" alt="image" src="https://github.com/user-attachments/assets/6e2c30a2-9f93-4bac-9e9b-2861fc9bb5a5" />

## lab walkthrough
### Installing docker and testing
1. Install docker using this command
```
sudo apt install docker.io -y
```

<img width="1907" height="522" alt="image" src="https://github.com/user-attachments/assets/fe416e29-3a66-4248-b017-fc3ab08c664c" />


2. Testing docker by this command
```
sudo docker run hello-world
```
**output**

<img width="1474" height="928" alt="image" src="https://github.com/user-attachments/assets/720d10b3-f955-4a34-9026-29406653700c" />

Get more command in [docker cli cheatsheet](https://docs.docker.com/get-started/docker_cheatsheet.pdf)

### Docker vs docker-compose
#### Docker
1. You can deploy a conatiner from an image using docker.
Create a `dockerfile`
```
# Use official Nginx image
FROM nginx:alpine

# Expose port 80 for web traffic
EXPOSE 80
```
<img width="1906" height="952" alt="image" src="https://github.com/user-attachments/assets/ae157c00-dc13-48bb-a601-a59a9a76bb14" />

Build it and run
```
# Build the image
docker build -t nginx-test .

# Run the container
docker run -d -p 8080:80 nginx-test
```
<img width="1107" height="149" alt="image" src="https://github.com/user-attachments/assets/185619c6-c16e-4c1f-9088-4482ab4cc267" />
<img width="1204" height="828" alt="image" src="https://github.com/user-attachments/assets/798b8188-7c91-4e36-a8f7-b0c710ff510a" />

2. Run without a `dockerfile` 

With docker, you can run directly docker image that other has already build. 
```
docker run -d -p 8081:80 nginx:alpine
```
<img width="1397" height="536" alt="image" src="https://github.com/user-attachments/assets/e9506649-e6c4-4f5d-b54b-42851ad80458" />
<img width="1329" height="822" alt="image" src="https://github.com/user-attachments/assets/d3591c79-2fb5-43a6-ba85-601103edc51b" />
### Docker compose

With docker compose, you can run multiple image and link it to each other. Here are sample of `docker-compose.yml`

```
version: '2'
services:
  application:
    image: euclid1990/ubuntu-server
    volumes:
      - ./blog:/var/www/html/blog
  mariadb:
    image: mariadb
    ports:
      - "3696:3306"
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: mydb
      MYSQL_USER: guest
      MYSQL_PASSWORD: 123456Aa@
    volumes:
      - ./mariadb:/var/lib/mysql
  php:
    image: php:7.2-fpm
    ports:
      - "9696:9000"
    volumes_from:
      - application
    links:
      - mariadb:mysql
    tty: true
  nginx:
    image: nginx
    ports:
      - "8696:80"
    links:
      - php
    volumes_from:
      - application
    volumes:
      - ./logs/nginx/:/var/log/nginx
      - ./nginx_conf:/etc/nginx/conf.d
```

## Installing REMnux docker container
1. Choose your container [here](https://hub.docker.com/u/remnux)
<img width="2877" height="1344" alt="image" src="https://github.com/user-attachments/assets/8fb1d1e1-ee03-4c66-bac0-f2924f3b5b97" />

I will test it with `remnux/rizin`
```
# pull the image
docker pull remnux/rizin:latest

# run an interactive shell as root (default)
docker run --rm -it --name rizin-shell remnux/rizin:latest bash
```
<img width="1338" height="252" alt="image" src="https://github.com/user-attachments/assets/95e39a21-feda-4fa8-ba8d-2f799569bc3c" />

## Reference
* [REMnux documentation](https://docs.remnux.org/run-tools-in-containers/remnux-containers#thug)
* [Docker hub REMnux](https://hub.docker.com/u/remnux)
* [What is docker](https://docs.docker.com/get-started/docker-overview/)
* [Docker vs Virtual Machine (VM) – Key Differences You Should Know](https://www.freecodecamp.org/news/docker-vs-vm-key-differences-you-should-know/)
* [Docker vs Docker-compose](https://viblo.asia/p/docker-vs-docker-compose-RnB5pXGd5PG)
* [Docker hello world](https://hub.docker.com/_/hello-world)
* [CLI Cheat Sheet](https://docs.docker.com/get-started/docker_cheatsheet.pdf)
* [Installing Docker on Kali Linux](https://www.kali.org/docs/containers/installing-docker-on-kali/)


