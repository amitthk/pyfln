#!/bin/bash

if (($# <4))
  then
    echo "Usage : $0 <DOCKER_PROJECT_NAME> <APP_NAME> <IMAGE_TAG> <directory containing k8s files>"
    exit 1
fi

main(){
find $4/*.yml -type f -exec sed -i.bak 's#__PROJECT_NAME__#'$1'#' {} \;
find $4/*.yml -type f -exec sed -i.bak 's#__APP_NAME__#'$2'#' {} \;
find $4/*.yml -type f -exec sed -i.bak  's#__IMAGE__#'$3'#' {} \;
}

