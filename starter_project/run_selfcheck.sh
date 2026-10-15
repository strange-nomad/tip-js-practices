#!/bin/bash
rm -rf out
mkdir -p out
find src -name "*.java" > sources.txt
javac -encoding UTF-8 -d out @sources.txt
rm sources.txt
java -cp out ru.edu.pr01.SelfCheck
