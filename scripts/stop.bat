@echo off
echo Stopping Project Management MVP...
docker stop pm-mvp-container
docker rm pm-mvp-container
echo Container stopped and removed.
pause