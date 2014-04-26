# Standard imports
import os


home = os.environ['HOME']
rc_dir_path = os.path.join(home, '.queuer')
if not os.path.exists(rc_dir_path):
    os.makedirs(rc_dir_path)

db_path = os.path.join(rc_dir_path, 'queuer.db')
dl_path = os.path.join(home, "downloads")
