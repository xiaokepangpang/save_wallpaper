::�ر���������Ļ���
@echo off
::���ñ��ر���
setlocal
::����ͼƬ����·�����޸ĵ�ַ�Ļ�ֻ��Ҫ�޸���һ�����ɣ�����б���Ǳ����
set target_dir=%HOMEPATH%\Pictures\wallpaper\
::���û���·������filterʱ������С��Ч�ʼӿ죩
set target_dir_temp=%target_dir%temp\
::��Windows�۽��ı�ֽȫ�����浽����·����
xcopy %localappdata%\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets %target_dir_temp% /y
::��������·����
pushd %target_dir_temp%
::ͨ��ѭ�����˵���С���ļ���300KB��
for /r %%i in (*) do @(if %%~zi lss 300000 del "%%i" /f)
::��ʣ��������ļ����Ϻ�׺��.jpg��
ren *.* *.jpg
::�˳�����·��
popd
::������·���µ��ļ�����ֽ��ȫ��������Ŀ���ļ����ļ��ظ�ʱֱ�Ӹ���
xcopy %target_dir_temp:~0,-1% %target_dir% /d /y
::��Ĭģʽ����ջ���·��
del /Q %target_dir_temp%*
::�˳����ر�������
endlocal
::����
cls
::echo powerd by С������
::pause