import os
import ast
import pandas as pd
import numpy as np
from datetime import datetime
import time
import logging


level_config = {'debug': logging.DEBUG, 'info': logging.INFO} 

FILE_SIZE = 500
BYTES_PER_PKT = 1500.0*8
MILLISEC_IN_SEC = 1000.0
EXP_LEN = 1000  # millisecond

class Metric:
    def __init__(self,name,mi=1., lbd=1., mi_s=1.,log_level='debug'):
        self.name = name
        self.mi = mi
        self.lbd = lbd
        self.mi_s = mi_s
        
        log_level = level_config[log_level.lower()]
        logging.basicConfig(level=log_level)
        self.logger = logging.getLogger(__name__)
  
    def calc(self,listRate,listRebuffer):
        pass


    def tabulation(self,listQoE,scores = pd.DataFrame(),abrRule = 'abr Rule',prefix=''):
        scores_tmp = pd.DataFrame()
        scores_tmp['abr Rule'] = [ abrRule for i in listQoE]
        scores_tmp['Average value'] = np.asarray([i[0] for i in listQoE])
        scores_tmp['Metrics'] = [ self.name for i in listQoE]
        scores = scores.append(scores_tmp)
        scores_tmp = pd.DataFrame()
        scores_tmp['Average value'] = np.asarray([i[1] for i in listQoE])
        scores_tmp['Metrics'] = [ prefix+'_'+'Bitrate Utility' for i in listQoE]
        scores_tmp['abr Rule'] = [ abrRule for i in listQoE]
        scores = scores.append(scores_tmp)
        scores_tmp['Average value'] = np.asarray([i[2] for i in listQoE])
        scores_tmp['Metrics'] = [ prefix+'_'+'Smoothness Penalty' for i in listQoE]
        scores_tmp['abr Rule'] = [ abrRule for i in listQoE]
        scores = scores.append(scores_tmp)
        scores_tmp = pd.DataFrame()
        scores_tmp['Average value'] = np.asarray([i[3] for i in listQoE])
        scores_tmp['Metrics'] = [ prefix+'_'+'Rebuffering Penalty' for i in listQoE]
        scores_tmp['abr Rule'] = [ abrRule for i in listQoE]
        scores = scores.append(scores_tmp)
        scores_tmp = pd.DataFrame()
        scores_tmp['Average value'] = np.asarray([i[4] for i in listQoE])
        scores_tmp['Metrics'] = [ prefix+'_'+'Startup Delay' for i in listQoE]
        scores_tmp['abr Rule'] = [ abrRule for i in listQoE]
        scores = scores.append(scores_tmp)
        return scores 

class MetricQoElin(Metric):
    def __init__(self,name='',mi=1., lbd=1., mi_s=1.,log_level='debug'):
        super().__init__(name,mi, lbd, mi_s,log_level)
    
    def calc(self,listRate,listRebuffer):
        bitrateUtility = np.asarray(listRate).sum()
        startupDelay = self.mi_s*np.asarray(listRebuffer[0])
        rebufferingPenalty = self.mi*np.asarray(listRebuffer[1:]).sum()
        smoothnessPenalty = self.lbd*np.abs(np.asarray(listRate[1:])-np.asarray(listRate[:-1])).sum()
        qoe = bitrateUtility - (smoothnessPenalty + rebufferingPenalty + startupDelay)
        # print(qoe)
        return qoe,bitrateUtility,smoothnessPenalty,rebufferingPenalty,startupDelay

class MetricQoEMean(Metric):
    def __init__(self,name='',mi=1., lbd=1., mi_s=1.,log_level='debug'):
        super().__init__(name,mi, lbd, mi_s,log_level)
    
    def calc(self,listRate,listRebuffer):
        bitrateUtility = np.asarray(listRate[1:])
        startupDelay = self.mi_s*np.asarray(listRebuffer[0])
        rebufferingPenalty = self.mi*np.asarray(listRebuffer[1:])
        smoothnessPenalty = self.lbd*np.abs(np.asarray(listRate[1:])-np.asarray(listRate[:-1]))
        qoe = bitrateUtility - (smoothnessPenalty + rebufferingPenalty + startupDelay)
        # print(qoe.sum())
        return qoe.sum(),bitrateUtility.sum(),smoothnessPenalty.sum(),rebufferingPenalty.sum(),startupDelay.sum()

class MetricQoElog(Metric):
    def __init__(self,name='',mi=1., lbd=1., mi_s=1.,log_level='debug'):
        super().__init__(name+'_'+'QoE_log',mi, lbd, mi_s,log_level)

    def calc(self,listRate,listRebuffer):
        bitrateUtility = np.log(np.asarray(listRate)/np.asarray(listRate).min()).sum()
        startupDelay = self.mi_s*np.asarray(listRebuffer[0])
        rebufferingPenalty = self.mi*np.asarray(listRebuffer[1:]).sum()
        smoothnessPenalty = self.lbd*np.abs(np.log(np.asarray(listRate[1:])/np.asarray(listRate[1:]).min()) \
                      - np.log(np.asarray(listRate[:-1])/np.asarray(listRate[1:]).min())).sum()
        qoe=bitrateUtility - (smoothnessPenalty + rebufferingPenalty + startupDelay)
        return qoe,bitrateUtility,smoothnessPenalty,rebufferingPenalty,startupDelay


class MetricQoEhd(Metric):
    def __init__(self,name='',mi=1., lbd=1., mi_s=1.,log_level='debug'):
        super().__init__(name+'_'+'QoE_hd',mi, lbd, mi_s,log_level)

    def calc(self,listRate,listRebuffer):
        bitrateUtility = (np.asarray(listRate)*100).mean()
        rebufferingPenalty = self.rebufferPenalty*(np.asarray(listRebuffer)).mean()
        smoothnessPenalty = np.abs((np.asarray(listRate[1:])*100)-(np.asarray(listRate[:-1])*100)).mean()
        qoe=(np.asarray(listRate)*100).sum()-self.rebufferPenalty*(np.asarray(listRebuffer)).sum()-np.abs((np.asarray(listRate[1:])*100)-(np.asarray(listRate[:-1])*100)).sum()
        return qoe,bitrateUtility,rebufferingPenalty,smoothnessPenalty


def parseLogs(metricQoE,path = '../results-collector/abrBola/',log_level='info',div_by=1e3):
    log_level = level_config[log_level.lower()]
    logging.basicConfig(level=log_level)
    logger = logging.getLogger(__name__)

    files = os.listdir(path)
    listQoE = []
    for file in files:
        # print(path+file)
        f = open(path+file, 'r')
        lines = f.readlines()
        logs = []
        i=0
        for line in lines:
            logs.append(ast.literal_eval(line.strip()))
            #print("bitrate: {} rebufferTime: {}".format(logs[i]['bitrate'],logs[i]['rebufferTime']))
            i+=1
        # print("Count segments: {}".format(i))
        df = pd.DataFrame(logs)
        #print(df['bitrate']/1e6,df['rebufferTime'])
        mt = metricQoE.calc(df['bitrate']/div_by,df['rebufferTime'])
        logger.debug(mt)
        listQoE.append(mt)
    return listQoE

def parseLogsBy(path = '../results-collector/abrBola',file_type='json',log_level='debug'):
    log_level = level_config[log_level.lower()]
    logging.basicConfig(level=log_level)
    logger = logging.getLogger(__name__)
    frames = []
    for dirpath, subdirpath, filenames in os.walk(path):
        client = 0
        for filename in [f for f in filenames if any(filetype in f.lower() for filetype in [file_type])]:
            current_file = os.path.join(dirpath, filename)
            logger.debug(current_file)
            f = open(current_file, 'r')
            lines = f.readlines()
            logs = []
            for line in lines:
                logs.append(ast.literal_eval(line.strip()))
            df = pd.DataFrame(logs)
            df['scenario'] = dirpath.split('/')[-2]
            df['abr Rule'] = filename.split('_')[1]
            df['client'] = client
            df['calc_bitrate'] = (((df['totalBytesLength']*8)/1000)/df['mediaduration'])
            frames.append(df)
            client +=1
    result = pd.concat(frames)
    return result


def writeTrace(output=None,df=None):
    t = df.Timestamp.apply(lambda x: time.mktime(datetime.strptime(x, "%Y.%m.%d_%H.%M.%S").timetuple()))
    bw = df['DL_bitrate']
    dfbw = pd.DataFrame()
    dfbw['time']=range(0,len(t))
    dfbw['DL_bitrate']=bw.reset_index(drop=True)
    dfbw.to_csv(output,index=False)

def parseTraces(input_path = '../../traces/5G-production-dataset/5G-production-dataset/Amazon_Prime/Driving/',
    output_path=None,minimum=0,maximum=1e15,file_type='csv',parameter='DL_bitrate',log_level='info'):
    log_level = level_config[log_level.lower()]
    logging.basicConfig(level=log_level)
    logger = logging.getLogger(__name__)
    frames = []
    for dirpath, subdirpath, filenames in os.walk(input_path):
        for filename in [f for f in filenames if any(filetype in f.lower() for filetype in [file_type])]:
            current_file = os.path.join(dirpath, filename)
            logger.debug("input file: {}".format(current_file))
            df = pd.read_csv(current_file)
            if output_path is not None:
                df = df[(df[parameter] >= minimum) & (df[parameter] <= maximum) ]
                logger.debug("output file: {}".format(output_path+filename))
                writeTrace(output=output_path+filename,df=df)
            frames.append(df)
    result = pd.concat(frames)
    return result

def maker_mahimahi_trace(IN_FILE = None,OUT_FILE = None):
    files = os.listdir(IN_FILE)
    for trace_file in files:
        if os.stat(IN_FILE + trace_file).st_size >= FILE_SIZE:
            df = pd.read_csv(IN_FILE + trace_file)
            with open(OUT_FILE + trace_file, 'w') as mf:
                millisec_time = 0
                mf.write(str(millisec_time) + '\n')
                for i in range(1,len(df.DL_bitrate)):
                    throughput = (float(df.DL_bitrate[i])*1000)
                    pkt_per_millisec = throughput / BYTES_PER_PKT / MILLISEC_IN_SEC
                    #print("pkt_per_millisec: {}".format(pkt_per_millisec))
                    millisec_count = 0
                    pkt_count = 0
                    while True:
                        millisec_count += 1
                        millisec_time += 1
                        to_send = (millisec_count * pkt_per_millisec) - pkt_count
                        to_send = np.floor(to_send)
                        #print("to_send: {}".format(to_send))
                        for i in range(int(to_send)):
                            mf.write(str(millisec_time) + '\n')
                            # print(millisec_time)
                        pkt_count += to_send
                        if millisec_count >= EXP_LEN:
                            break