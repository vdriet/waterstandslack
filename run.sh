cd /home/peter/dev/waterstandslack
docker stop waterstandslack
docker rm -f waterstandslack
docker run \
	--detach \
	--name waterstandslack \
	--env-file env.list \
	waterstandslack
