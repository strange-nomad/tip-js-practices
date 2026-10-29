@echo off
chcp 65001 >nul
where javac >nul 2>&1
if %errorlevel% neq 0 (
    if exist "%ProgramFiles%\Eclipse Adoptium\jdk-21.0.12.101-hotspot\bin" (
        set "PATH=%ProgramFiles%\Eclipse Adoptium\jdk-21.0.12.101-hotspot\bin;%PATH%"
    )
)
if exist out rmdir /s /q out
mkdir out
javac -encoding UTF-8 -d out src\ru\edu\pr03\*.java
java -cp out ru.edu.pr03.SelfCheck
