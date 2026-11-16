#!/bin/bash
# 本机 <-> home-server（生成环境）同步。在仓库任意位置运行均可：
#   bash tools/build-env/sync.sh push N           把 code/project0N、tools/projectN-build、tools/review、docs/requirements 推到服务器
#                                                 （文本文件转 LF、文件权限按 git 的记录恢复；只覆盖、不删除，本机删掉的文件提交后用 bundle 清掉）
#   bash tools/build-env/sync.sh pull-code N      取回服务器上的实测结果 .wout/.wret/.wdiag/.wcap/.wcapret
#                                                 （在服务器上跑完 wrun.sh 后先取回再 push，否则本机没有的新结果会被旧文件覆盖）
#   bash tools/build-env/sync.sh pull-build N DIR 取回 tools/projectN-build 的 build/ 与 fig/ 到本机 DIR
#   bash tools/build-env/sync.sh run '命令'        在服务器的生成环境容器里运行命令（工作目录 /work，即仓库根目录）
#   bash tools/build-env/sync.sh bundle           用增量 git bundle 把服务器仓库切到本机的 main（服务器不能访问 GitHub）
# 服务器用环境变量指定（仓库公开，地址不写进脚本）：
#   HOME_SERVER=用户@主机（必填）  HOME_SERVER_KEY=私钥文件（可选）  HOME_SERVER_REPO=服务器上的仓库目录（默认 ~/ai-c-textbook）
set -e
[ -n "$HOME_SERVER" ] || { echo "请先设置 HOME_SERVER=用户@主机（可选 HOME_SERVER_KEY=私钥文件）" >&2; exit 1; }
SSH=(ssh -o BatchMode=yes -o StrictHostKeyChecking=yes -o ServerAliveInterval=30)
[ -z "$HOME_SERVER_KEY" ] || SSH+=(-i "$HOME_SERVER_KEY" -o IdentitiesOnly=yes)
SSH+=("$HOME_SERVER")
REPO=${HOME_SERVER_REPO:-'~/ai-c-textbook'}
cd "$(dirname "$0")/../.."
proj() {  # 项目号 -> code/project0N、tools/projectN-build
  case "$1" in ''|*[!0-9]*) echo "项目号要写数字，如 6" >&2; exit 1 ;; esac
  CODE=code/project$(printf %02d "$((10#$1))"); TOOL=tools/project$((10#$1))-build
}
case "$1" in
push)
  proj "$2"
  tar --exclude=build --exclude=fig --exclude=__pycache__ -cf - "$CODE" "$TOOL" tools/review docs/requirements |
    "${SSH[@]}" "cd $REPO && tar -xmf - && find $CODE $TOOL tools/review -type f \( -name '*.sh' -o -name '*.py' -o -name '*.js' \
      -o -name '*.c' -o -name '*.in*' -o -name '*.cin' -o -name '*.txt' -o -name '.gitignore' \) -exec sed -i 's/\r\$//' {} + &&
      git diff --summary | sed -n 's/^ mode change 100644 => 100755 //p' | xargs -r -d '\n' chmod a-x &&
      git diff --summary | sed -n 's/^ mode change 100755 => 100644 //p' | xargs -r -d '\n' chmod a+x && echo pushed" ;;
pull-code)
  proj "$2"
  "${SSH[@]}" "cd $REPO && find $CODE -name '*.w*' | tar -cf - -T -" | tar -xf - && echo pulled ;;
pull-build)
  proj "$2"
  [ -n "$3" ] || { echo "要给出本机目录" >&2; exit 1; }
  mkdir -p "$3" && "${SSH[@]}" "cd $REPO/$TOOL && tar -cf - build fig" | tar -xf - -C "$3" && echo pulled-build ;;
run)
  "${SSH[@]}" "cd $REPO && bash tools/build-env/run.sh bash -c '$2'" ;;
bundle)
  H=$("${SSH[@]}" "cd $REPO && git rev-parse HEAD")
  if [ "$H" = "$(git rev-parse main)" ]; then echo "服务器已是本机 main：$(git log -1 --format='%h %s' main)"; exit 0; fi
  git merge-base --is-ancestor "$H" main || { echo "服务器的 $H 不在本机 main 的历史中，请先人工核对" >&2; exit 1; }
  B=$(mktemp -d)/main.bundle
  git bundle create -q "$B" "$H..main"
  "${SSH[@]}" "cat > /tmp/ai-c-textbook.bundle" < "$B" && rm -rf "$(dirname "$B")"
  "${SSH[@]}" "cd $REPO && echo '服务器上未提交的改动（将被 main 覆盖）：' && git status --short &&
    git fetch -q /tmp/ai-c-textbook.bundle main:refs/remotes/bundle/main && git checkout -q -f -B main refs/remotes/bundle/main &&
    rm -f /tmp/ai-c-textbook.bundle && git log -1 --format='服务器已同步到 %h %s' && echo '未跟踪的文件（如需清理请人工处理）：' && git clean -nd" ;;
*)
  sed -n '2,11p' "$0" >&2; exit 1 ;;
esac
