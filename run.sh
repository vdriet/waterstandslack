. ./setslackenv.sh
docker stop waterstandslack
docker rm -f waterstandslack
docker run \
	--detach \
	--name waterstandslack \
	--env SLACK_ID_RASPBOT=${SLACK_ID_RASPBOT} \
	waterstandslack
