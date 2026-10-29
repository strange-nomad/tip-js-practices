#!/bin/bash
rm -rf out
mkdir -p out
javac -encoding UTF-8 -d out src/ru/edu/pr02/*.java
java -cp out ru.edu.pr02.SelfCheck
