#creating the logs directory to store log in files
import os
import logging
from datetime import datetime
log_dir = "logs"
os.makedirs(log_dir,exist_ok=True)

#creating the file name according to the time stamp

current_time_stamp = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
file_name = f"log_{current_time_stamp}.log"

#creating the file

log_file_path = os.path.join(log_dir,file_name)

logging.basicConfig(
    filename=log_file_path,
    filemode="w",
    format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

