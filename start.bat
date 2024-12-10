@echo off

title CuluMod Installer ^| V0.1.2

echo Installing...
pip install colorama --user -q --no-warn-script-location
pip install requests --user -q --no-warn-script-location
pip install wmi --user -q --no-warn-script-location
echo Installing Complete!


set script_dir=%~dp0
cls
start %script_dir%\Bin\culu\dist\main\v000348000030\const.py
exit