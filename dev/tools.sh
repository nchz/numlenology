#!/bin/bash -e

PROJECT_NAME=$(basename `git config --get remote.origin.url` | sed 's/.git$//')
PROJECT_ROOT_DIR=`git rev-parse --show-toplevel`

DOCKER_IMAGE_TAG=${DOCKER_IMAGE_TAG:-'dev'}
DOCKER_IMAGE_NAME=${PROJECT_NAME}:${DOCKER_IMAGE_TAG}

# parse arguments.
cmd=$1
shift

case ${cmd} in
    h | help)
        # self-print to stdout.
        cat $0 | less
        ;;

    b | build)
        docker build \
            -t ${DOCKER_IMAGE_NAME} \
            $@ ${PROJECT_ROOT_DIR}
        ;;

    r | run)
        docker run -it --rm \
            --name ${PROJECT_NAME} \
            -p 8888:8888 \
            -v ${PROJECT_ROOT_DIR}/src:/src \
            ${DOCKER_IMAGE_NAME} \
            jupyter lab \
                --ip 0.0.0.0 \
                --allow-root \
                --NotebookApp.token=''
        ;;

    s | shell)
        # open bash inside a running container of the project.
        docker exec -it \
            ${PROJECT_NAME} /bin/bash
        ;;

    *)
        echo "Bad command. Options are:"
        grep -E "^    . \| .*\)$" $0
    ;;

esac
