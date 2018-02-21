echo "unpacking UI package"
tar -xvf ~/kryptedauth/bin/ui_files.tar
echo "moving UI folder to static"
mv ~/kryptedauth/bin/ui/ ~/kryptedauth/app/static/global/
