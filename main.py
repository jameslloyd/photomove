import dropbox
import re
import os
import datetime, time
import logging, sys, json
from dotenv import load_dotenv

# Create a logger
logger = logging.getLogger()

# Set the log level to include all messages
logger.setLevel(logging.DEBUG)

# Create a handler for stdout
handler = logging.StreamHandler(sys.stdout)

# Create a formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add the formatter to the handler
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)


load_dotenv()
DROPBOX_TOKEN = os.getenv('DROPBOX_TOKEN')
PHOTOS_DIR = os.getenv('PHOTOS_DIR')
DROPBOX_CAMERA_UPLOADS_DIR1 = os.getenv('DROPBOX_CAMERA_UPLOADS_DIR1')
DROPBOX_CAMERA_UPLOADS_DIR2 = os.getenv('DROPBOX_CAMERA_UPLOADS_DIR2')
CHECK_EVERY = int(os.getenv('CHECK_EVERY'))

dbx = dropbox.Dropbox(DROPBOX_TOKEN)

def list_files(path):
    for entry in dbx.files_list_folder(path).entries:
        # strip the file extension from the file name
        file_name = os.path.splitext(entry.name)[0]
        if re.match(r'\d{4}-\d{2}-\d{2} \d{2}.\d{2}.\d{2}', file_name):

            split_name = file_name.split(' ')
            date = split_name[0].split('-')
            year = date[0]
            month = date[1]
            # change month to name using datetime module
            month_name = datetime.datetime.strptime(month, "%m").strftime("%B")
            day = date[2]
            # check if file exists with same name in local directory
            localphotopath = os.path.join(PHOTOS_DIR,year,month,f'{day} {month_name} {year}',entry.name)
            if os.path.isfile(localphotopath):
                logger.info(f'{entry.name} already exists deleting from dropbox...')
                # delete the file from dropbox
                dbx.files_delete_v2(path + '/' + entry.name)
            else:
                logger.info(f'Downloading {entry.name}...')
                dbx.files_download_to_file(localphotopath, path + '/' + entry.name)

    
# loop to check files every 10 minutes
while True:
    for dir in [DROPBOX_CAMERA_UPLOADS_DIR1, DROPBOX_CAMERA_UPLOADS_DIR2]:
        logging.info(f'Checking {dir} for files...')
        list_files(dir)
    logging.info(f'Sleeping for {CHECK_EVERY / 60} minutes...')
    time.sleep(CHECK_EVERY)