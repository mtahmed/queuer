# Standard imports
import os


HOME = os.environ['HOME']
rc_dir_path = os.path.join(HOME, '.thepiratebay')
if not os.path.exists(rc_dir_path):
    os.makedirs(rc_dir_path)

db_path = rc_dir_path + 'thepiratebay.tpb'
