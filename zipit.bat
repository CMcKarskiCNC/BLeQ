@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM Base directory
set "BASEDIR=%~dp0"
set "BASEDIR=%BASEDIR:~0,-1%"

REM Read ZIP name
if not exist "%BASEDIR%\name.txt" (
    echo ERROR: name.txt not found
    pause
    exit /b 1
)

for /f "usebackq delims=" %%N in ("%BASEDIR%\name.txt") do set "ZIPNAME=%%N"
if "%ZIPNAME%"=="" (
    echo ERROR: name.txt is empty
    pause
    exit /b 1
)

REM Staging folder
set "STAGE=%BASEDIR%\__zip_stage__"

powershell -NoProfile -Command ^
  "$base='%BASEDIR%';" ^
  "$stage='%STAGE%';" ^
  "$zip=Join-Path $base '%ZIPNAME%';" ^
  "$ex=@('%~nx0','exclude.txt','name.txt','%ZIPNAME%');" ^
  "if(Test-Path (Join-Path $base 'exclude.txt')){ $ex += Get-Content (Join-Path $base 'exclude.txt') };" ^
  "if(Test-Path $stage){Remove-Item $stage -Recurse -Force};" ^
  "New-Item -ItemType Directory -Path $stage | Out-Null;" ^
  "Get-ChildItem $base -Force | Where-Object { $_.Name -ne '__zip_stage__' } | ForEach-Object {" ^
  "  $root = $_;" ^
  "  $rootRel = $root.FullName.Substring($base.Length+1);" ^
  "  foreach($e in $ex){ if($rootRel -eq $e -or $rootRel -like \"$e\\*\"){ return } };" ^
  "  Get-ChildItem $root.FullName -Recurse -Force | ForEach-Object {" ^
  "    $rel=$_.FullName.Substring($base.Length+1);" ^
  "    foreach($e in $ex){ if($rel -eq $e -or $rel -like \"$e\\*\"){ return } };" ^
  "    $dest=Join-Path $stage $rel;" ^
  "    if($_.PSIsContainer){ New-Item -ItemType Directory -Path $dest -Force | Out-Null }" ^
  "    else{ New-Item -ItemType Directory -Path (Split-Path $dest) -Force | Out-Null; Copy-Item $_.FullName $dest }" ^
  "  }" ^
  "};" ^
  "if(Test-Path $zip){Remove-Item $zip};" ^
  "Compress-Archive -Path (Join-Path $stage '*') -DestinationPath $zip -CompressionLevel NoCompression;" ^
  "Remove-Item $stage -Recurse -Force"

echo Done: %ZIPNAME%
pause
