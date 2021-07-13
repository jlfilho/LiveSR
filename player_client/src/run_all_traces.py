import os
import time
import subprocess
import logging
import yaml

with open("config/config.yml", "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)
log_level = cfg["enviroment"]["log_level"]
cfg  =cfg["player_client"]
# Enviroment
level_config = {'debug': logging.DEBUG, 'info': logging.INFO} 
log_level = level_config[log_level.lower()]
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)

abr_algo = cfg["session"]["abr_algo"]
run_time = cfg["session"]["run_time"]
os.system('sudo sysctl -w net.ipv4.ip_forward=1')


RUN_SCRIPT = 'run_traces.py'

processes = []
for abr in abr_algo:
	try:
		command = 'python3 ' + RUN_SCRIPT + ' ' + abr 
		proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
		processes.append(proc)
		time.sleep(1)
	except Exception as e:
		logger.debug("Erro to run {}".format(command))
		logger.debug("Error info {}".format(e))

for proc in processes:
	proc.wait()
	proc.kill()