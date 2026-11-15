#!/bin/sh
# wrun.sh 用 DISPLAY=:99；结束后把挂载进来的仓库交还宿主用户，免得留下 root 文件
Xvfb :99 -screen 0 1280x1024x24 >/dev/null 2>&1 &
"$@"; s=$?
[ -n "$HOST_UID" ] && chown -R "$HOST_UID:$HOST_GID" /work
exit $s
