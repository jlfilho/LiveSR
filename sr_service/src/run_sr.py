import sys
import os
import yaml
import subprocess
import logging
import time


with open("config/config.yml", "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)
log_level = cfg["enviroment"]["log_level"]
cfg  =cfg["sr_service"]

MM_DELAY = cfg["channel_to_ingest"]["mm_delay"]   # millisec
downlink = cfg["channel_to_ingest"]["downlink"]
uplink = cfg["channel_to_ingest"]["uplink"]

# Enviroment
timeout = None if cfg["enviroment"]["timeout"] == "None" else int(cfg["enviroment"]["timeout"])

level_config = {'debug': logging.DEBUG, 'info': logging.INFO} 
log_level = level_config[log_level.lower()]
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)

RUN_SCRIPT = 'sr_service.py'
os.system('sudo sysctl -w net.ipv4.ip_forward=1')

def main():
    while (True):
        logger.debug('mm-delay ' + str(MM_DELAY) + 
            ' mm-link '  + uplink +' '+   downlink +' ' +
            'python3 ' + RUN_SCRIPT)
        args = ['mm-delay', str(MM_DELAY), 'mm-link', uplink,downlink, 'python3', RUN_SCRIPT]
        proc = subprocess.Popen(args,stdin=subprocess.PIPE)
        logger.info('Super-resolution Started ')
        try:
            result = proc.wait()
            if result != 0:
                raise NameError('SR cased a error.\nRestarting...') 
        except NameError as e:
            proc.kill()
            logger.info("Error: {}.".format(str(e)))
            time.sleep(5)
        except KeyboardInterrupt as e:
            proc.kill()
            logger.info("KeyboardInterrupt: {}.".format("Transmission closed"))
            exit()
        finally:
            proc.kill()

if __name__ == '__main__':
	main()