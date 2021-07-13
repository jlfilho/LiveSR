import os
import sys
import subprocess
import logging
import yaml
import numpy as np
import time
from pyvirtualdisplay import Display

abr_algo = sys.argv[1]

RUN_SCRIPT = 'run_video.py'


with open("config/config.yml", "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)
log_level = cfg["enviroment"]["log_level"]
cfg  =cfg["player_client"]
# Enviroment
level_config = {'debug': logging.DEBUG, 'info': logging.INFO} 
log_level = level_config[log_level.lower()]
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)

downlink_trace_path = cfg["channel_to_delivery"]["traces_downlink"]
uplink_trace = cfg["channel_to_delivery"]["uplink"]
mm_delay = cfg["channel_to_delivery"]["mm_delay"]

run_time = cfg["session"]["run_time"]
visibleInVirtualDisplay = cfg["session"]["visible_virtual_display"]

os.system('sudo sysctl -w net.ipv4.ip_forward=1')

def main():
	sleep_vec = list(range(1, 10))  # random sleep second
	files = os.listdir(downlink_trace_path)
	processes = []
	process_id = 0
	display = []
	for f in files:
		if visibleInVirtualDisplay:
			command = 'mm-delay ' + mm_delay + ' mm-link ' + uplink_trace + ' ' + downlink_trace_path + f + ' --meter-downlink' + \
				' python3 ' + RUN_SCRIPT + ' ' + abr_algo + ' ' + abr_algo + '_' + str(process_id)
		else:
			command = 'mm-delay ' + mm_delay + ' mm-link ' + uplink_trace + ' ' + downlink_trace_path + f + \
				' python3 ' + RUN_SCRIPT + ' ' + abr_algo + ' ' + abr_algo + '_' + str(process_id)

		process_id+=1
		logger.debug('\n\t{}'.format(command)) 
		time.sleep(0.2)
		disp = Display(visible=visibleInVirtualDisplay, size=(900,1000),manage_global_env=False)
		disp.start()
		display.append(disp)
		try:
			proc = subprocess.Popen(command,
				stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=disp.env(),shell=True)
			processes.append(proc)
		except KeyboardInterrupt as e:
			for p in processes:
				p.kill() 
			logger.info("KeyboardInterrupt: {}.".format("closed"))
			exit() 
		except Exception as e:
			logger.debug("Erro to run {}".format(command))
			logger.debug("Error info {}".format(e))
			time.sleep(1)

	i=0
	for proc in processes:
		result = proc.communicate()
		display[i].stop()
		i+=1
		logger.debug("Info {}".format(result))
			

if __name__ == '__main__':
	main()