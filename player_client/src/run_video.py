import sys
import logging
import yaml
from video_session import video_session


abr_algo = sys.argv[1]
process_id = sys.argv[2]

with open("config/config.yml", "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)
log_level = cfg["enviroment"]["log_level"]
key = cfg["enviroment"]["key"]
cfg  =cfg["player_client"]
# Enviroment
level_config = {'debug': logging.DEBUG, 'info': logging.INFO} 
log_level = level_config[log_level.lower()]
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)

run_time = cfg["session"]["run_time"]
url = cfg["session"]["url"]+'/live/'+abr_algo +  '_index.html'
url_mpd = cfg["session"]["url"]+'/dash/'+key+'.mpd'
default_chrome_user_dir = cfg["session"]["default_chrome_user_dir"]
chrome_driver = cfg["session"]["chrome_driver"]

try:
	# start video session
	video_session(url, process_id,run_time, default_chrome_user_dir, chrome_driver,url_mpd)
	print('done')
except Exception as e:
	print(e)