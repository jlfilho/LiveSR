import subprocess
import logging
import yaml


with open("config/config.yml", "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)
log_level = cfg["enviroment"]["log_level"]
key = cfg["enviroment"]["key"]
cfg  =cfg["sr_service"]
# Enviroment
timeout = None if cfg["enviroment"]["timeout"] == "None" else int(cfg["enviroment"]["timeout"])
level_config = {'debug': logging.DEBUG, 'info': logging.INFO} 
log_level = level_config[log_level.lower()]
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)


# RTMP servers address
ingest_server = cfg["ingest_server"]["server"]+":"+cfg["ingest_server"]["port"]+"/"+cfg["ingest_server"]["channel"]+"/"+key 
transcode_service = cfg["transcode_service"]["server"]+":"+cfg["transcode_service"]["port"]+"/"+cfg["transcode_service"]["channel"]+"/"+key


def sr_escpn(ingest_server,transcode_service,bufsize=5*1000000):
    logger.debug('Starting SR Upscale')
    args = ['/usr/local/bin/ffmpeg', '-i', ingest_server, '-filter_complex', '[0:v] format=pix_fmts=yuv420p, extractplanes=y+u+v [y][u][v]; [y] sr=dnn_backend=tensorflow:scale_factor=2:model=/models/espcn.pb [y_scaled]; [u] scale=iw*2:ih*2 [u_scaled]; [v] scale=iw*2:ih*2 [v_scaled]; [y_scaled][u_scaled][v_scaled] mergeplanes=0x001020:yuv420p [merged]', '-map',
 '[merged]', '-sws_flags', 'lanczos', '-c:v', 'libx264', '-crf', '17', '-c:a', 'copy', '-f', 'flv', transcode_service]
    return subprocess.Popen(args,stdin=subprocess.PIPE, bufsize=bufsize)


sr =  sr_escpn(ingest_server,transcode_service)

try:  
    result = sr.wait(timeout=timeout)
    if result != 0:
        raise NameError('ConnectionError')
except subprocess.TimeoutExpired as e:
    logger.info("Error: {}.".format(str(e)))
except OSError as e: 
    logger.info("Error: {}.".format(str(e)))
except NameError as e:
    logger.info("Error: {}.".format(str(e)))
finally:
    sr.kill()
    