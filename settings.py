# Standard imports
import os


HOME = os.environ['HOME']
rc_dir_path = os.path.join(HOME, '.queuer')
if not os.path.exists(rc_dir_path):
    os.makedirs(rc_dir_path)

db_path = os.path.join(rc_dir_path, 'queuer.db')
