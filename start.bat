@echo off

title CuluMod Installer ^| V0.0.1

echo Installing...
pip install colorama --user -q --no-warn-script-location
pip install requests --user -q --no-warn-script-location
echo Installing Complete!


set script_dir=%~dp0

start %script_dir%\Bin\culu\dist\main\v000348000030\const.py