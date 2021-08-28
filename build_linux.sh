 #!/bin/bash  
APP_NAME="shimekiri"
MAIN_FILE_PATH=shimekiri/main.py
SITE_PACKAGES_PATH=.env/lib64/python3.9/site-packages
RES_FOLDER="./res:./res"
DEFAULT_CONFIG="default_config.json:."
ICON_PATH="./res/images/icons/death.ico"

python3 -m PyInstaller --onedir --windowed \
--icon $ICON_PATH \
--paths $SITE_PACKAGES_PATH \
--add-data=$RES_FOLDER \
--add-data=$DEFAULT_CONFIG \
-n $APP_NAME \
$MAIN_FILE_PATH

$SHELL 
