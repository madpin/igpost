#!/usr/bin/env bash

# function docker_run() {
#     P_dash=${P//\//\-}
#     docker build -f ./$P/Dockerfile -t "$P_dash" .
# 	docker run --env-file=".env" --name $P_dash --rm $P_dash:latest
# }

function update_deps() {
    echo "###############################################################"
    pip-compile --upgrade --output-file=requirements.frozen requirements.in
    pip-compile --upgrade --output-file=requirements.dev requirements.dev.in
}

# function list_ps() {
#     set -e
#     echo "###############################################################"
#     echo "       Valid Projects [folders]:"
#     echo "###############################################################"
#     echo
#     echo

#     for D in *; do
#         if [[ -d "${D}" ]]; then
#             FILE=${D}/__main__.py
#             if [[ -f "$FILE" ]]; then
#                 echo `dirname $FILE`
#                 # pip-compile --emit-index-url --upgrade --output-file=${FILE_FROZEN} $FILE
#             fi
#         fi
#     done
#     echo
#     echo "###############################################################"
# }

# function pre_commit() {
#     echo "#####################"
#     echo "pre-commit run --all-files"
#     pre-commit run --all-files

#     echo "#####################"
#     echo "Black"
#     black .

#     echo "#####################"
#     echo "Isort"
#     isort .

#     echo "#####################"
#     echo "Flake 8"
#     flake8 .
# }
