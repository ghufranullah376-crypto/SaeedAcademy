@echo off
title Add Real Photos to Saeed Academy Website
color 0A
echo.
echo =========================================================
echo   SAEED ACADEMY - Add Your Real Photos
echo =========================================================
echo.
echo Your website is ready! The images folder is:
echo.
echo   static\images\logo.png         ^<-- Replace with academy logo
echo   static\images\academy\ceo.jpg  ^<-- Replace with Saeed Wazir photo
echo   static\images\academy\gallery1.jpg  ^<-- Certificate ceremony group
echo   static\images\academy\gallery2.jpg  ^<-- Certificate presentation
echo   static\images\academy\gallery3.jpg  ^<-- New batch starting poster
echo   static\images\academy\gallery4.jpg  ^<-- World Peace Summit photo
echo   static\images\academy\gallery5.jpg  ^<-- Students in classroom
echo   static\images\academy\gallery6.jpg  ^<-- Welcome portrait
echo   static\images\academy\classroom.jpg ^<-- Red carpet learning
echo.
echo =========================================================
echo   STEPS TO ADD YOUR PHOTOS:
echo =========================================================
echo.
echo 1. Open the images folder:
explorer "%~dp0static\images"
echo.
echo 2. Simply COPY and PASTE (or drag) your real photos
echo    into the correct subfolder, renaming them to match
echo    the filenames above.
echo.
echo 3. The website will automatically show your real photos.
echo.
echo =========================================================
echo   The website is running at: http://localhost:5000
echo =========================================================
echo.
pause
