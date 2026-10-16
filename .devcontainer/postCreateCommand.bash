#!/bin/bash
# リポジトリに依存する処理だけを行う。ツールは Dockerfile でイメージに入れている

# デバッグ実行（launch.json）・run・グラフ可視化の標準入力。gitignore 対象
echo make input.txt and contests/
touch input.txt
mkdir -p contests

# build/ は名前付きボリューム（devcontainer.json の mounts）で root 所有で作られるため、所有者を変える
if [ -d build ] && [ "$(stat -c %u build)" != "$(id -u)" ]; then
    echo change owner of build
    sudo chown -R "$(id -u):$(id -g)" build
fi

g++ --version | head -n 1
python3 --version
pypy3 --version | tail -n 1
oj --version
