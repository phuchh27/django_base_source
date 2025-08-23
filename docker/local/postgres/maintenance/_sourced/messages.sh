#!/urs/bin/env bash

message_newline(){
  echo
}

message_debug(){
  echo -e "DEBUG: ${@}"
}

message_welcome(){
  echo -e "\e[1m${@}\e[0m"
}

message_warning(){
 echo -e "\e[33mWARNING\e[0m: ${@}"
}

message_error(){
 echo -e "\e[33mERROR\e[0m: ${@}"
}

