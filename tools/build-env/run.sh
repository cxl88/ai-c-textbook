#!/bin/sh
# 在生成环境容器里运行命令；仓库挂载为 /work。用法：tools/build-env/run.sh [命令…]（默认进 bash）
#   例：tools/build-env/run.sh bash -c 'cd book && python3 build.py'
# v5 版式模板放在 $PROJECT_FILES/textbook/v5/（默认 ~/ai-c-textbook-env/project-files），挂载为 /mnt/project-files。
R=$(cd "$(dirname "$0")/../.." && pwd)
PF=${PROJECT_FILES:-$HOME/ai-c-textbook-env/project-files}
[ -t 0 ] && T=-t
exec docker run --rm -i $T -e HOST_UID=$(id -u) -e HOST_GID=$(id -g) \
  -v "$R:/work" -v "$PF:/mnt/project-files:ro" ai-c-textbook-build "$@"
