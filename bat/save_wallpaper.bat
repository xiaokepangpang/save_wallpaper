::关闭所有命令的回显
@echo off
::设置本地变量
setlocal
::设置图片保存路径，修改地址的话只需要修改这一处即可，最后的斜杠是必需的
set target_dir=%HOMEPATH%\Pictures\wallpaper\
::设置缓存路径（做filter时基数减小，效率加快）
set target_dir_temp=%target_dir%temp\
::将Windows聚焦的壁纸全部保存到缓存路径下
xcopy %localappdata%\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets %target_dir_temp% /y
::进到缓存路径下
pushd %target_dir_temp%
::通过循环过滤掉过小的文件（300KB）
for /r %%i in (*) do @(if %%~zi lss 300000 del "%%i" /f)
::将剩余的所有文件加上后缀“.jpg”
ren *.* *.jpg
::退出缓存路径
popd
::将缓存路径下的文件（壁纸）全部拷贝到目标文件，文件重复时直接覆盖
xcopy %target_dir_temp:~0,-1% %target_dir% /d /y
::静默模式下清空缓存路径
del /Q %target_dir_temp%*
::退出本地变量环境
endlocal
::清屏
cls
::echo powerd by 小可胖胖
::pause