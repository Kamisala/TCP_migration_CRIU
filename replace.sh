#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Usage: $0 file.txt file2.txt"
    exit 1
fi

# 读取file2.txt中的内容
content=$(cat "$2")

# 将file2.txt中的内容替换为file.txt中的内容
echo "$content" > "$1"

echo "Content of $1 has been replaced with content of $2"
sudo chmod 777 $1
