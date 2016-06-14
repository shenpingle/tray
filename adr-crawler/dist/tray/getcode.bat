@echo off

cd ocr

java -d32 -classpath .;demo.jar;aspriseOCR.jar com.asprise.util.ocr.demo.Demo ../capacha.png "A general sample with both characters and barcodes" >> ../code2.txt
pause
		