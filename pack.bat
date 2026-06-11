@echo off
echo 正在打包 MarkItDown 转换器...

:: 清理旧文件
rmdir /s /q dist 2>nul
rmdir /s /q build 2>nul

:: 使用 PyInstaller 打包
pyinstaller ^
  --windowed ^
  --name MarkItDown-Converter ^
  --exclude-module matplotlib ^
  --exclude-module scipy ^
  --exclude-module PyQt5 ^
  --exclude-module tensorflow ^
  --exclude-module torch ^
  --exclude-module sklearn ^
  --exclude-module IPython ^
  --exclude-module notebook ^
  --exclude-module zmq ^
  --exclude-module gevent ^
  --exclude-module twisted ^
  --exclude-module sphinx ^
  --exclude-module sqlalchemy ^
  --exclude-module tables ^
  --exclude-module dask ^
  --exclude-module cv2 ^
  --exclude-module numba ^
  --exclude-module xarray ^
  --exclude-module pytest ^
  --exclude-module pandas ^
  --exclude-module openpyxl ^
  --exclude-module xlrd ^
  --exclude-module xlsxwriter ^
  --exclude-module numexpr ^
  --exclude-module mkl ^
  --exclude-module PyQt5.QtWebEngineWidgets ^
  --exclude-module PyQt5.QtWebEngineCore ^
  --exclude-module PyQt5.QtWebChannel ^
  --exclude-module PyQt5.QtPrintSupport ^
  --exclude-module PyQt5.QtSql ^
  --exclude-module PyQt5.QtNetwork ^
  --exclude-module PyQt5.QtXml ^
  --exclude-module PyQt5.QtSvg ^
  --exclude-module PyQt5.QtOpenGL ^
  --exclude-module PyQt5.QtMultimedia ^
  --exclude-module PyQt5.QtBluetooth ^
  --exclude-module PyQt5.QtPositioning ^
  --exclude-module PyQt5.QtWebSockets ^
  --exclude-module PyQt5.QtQuick ^
  --exclude-module PyQt5.QtQml ^
  simple-converter.py

echo 打包完成！
pause