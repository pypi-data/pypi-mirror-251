import os
import math
import time
import yaml
import random
import subprocess
from typing import Any
from copy import deepcopy
import torch, numpy, json
from subprocess import Popen
from datetime import datetime
from QUANTAVE.Criterions import *
from QUANTAVE.Optimizers import *
from QUANTAVE.Architectures import *
from QUANTAVE.Dataloaders.Pipeline import *


Round = lambda A, decimal=4: round(A, ndigits=decimal) if type(A)!=torch.Tensor else A.round(decimals=decimal)


class ChalkBoard(object):
    """ ChalkBoard Class """
    def __init__(self,
                 experiment_name:str) -> None:
        self.details_path = os.path.join(os.path.expanduser("~"), f"Results/{experiment_name.replace(' ', '_').upper()}")
        self.checkpoint_path = os.path.join(os.path.expanduser("~"), f"Results/{experiment_name.replace(' ', '_').upper()}/Checkpoints")
    
        self.file = os.path.join(self.details_path, "board.txt")
        self.experiment = experiment_name
        
        if not os.path.isdir(self.details_path):
            os.makedirs(self.details_path)
        if not os.path.isdir(self.checkpoint_path):
            os.makedirs(self.checkpoint_path)
        if not os.path.isfile(self.file):
            Popen(["touch", self.file])

        self.__initial_headers(self.file)
        
    def __datetime(self):
        data = str(datetime.now()).split()
        return " ".join([data[0], ":".join(data[-1].split(".")[0].split(":")[:2])])
    
    def __initial_headers(self, file:str):
        u = "_______"*16
        h = f"++++    ChalkBoard for Experiment [ {self.experiment} ]    ++++"
        t = self.__datetime()
        with open(file, "a") as F:
            F.write(h.center(120) + "\n")
            F.write(u.center(120) + "\n")
            F.write(t.center(120) + "\n")
            F.write(u.center(120) + "\n")
            F.write("\n")
            F.close()
    
    def scribe(self, *args):
        with open(self.file, "a") as F:
            F.write(f">>  {self.__datetime()}  >> " + ", ".join([str(i) for i in args]) + "\n")
            F.close()
    
    def subheading(self, *args):
        with open(self.file, "a") as F:
            F.write("_______"*16 + "\n")
            F.write(f">>  {self.__datetime()}  >> " + ", ".join([str(i) for i in args]) + "\n")
            F.write("_______"*16 + "\n")
            F.close()
    
    def seperaor(self,):
        with open(self.file, "a") as F: F.write("<|-|-|>"*16+"\n"); F.close()
    
    def write_json(self, json_data):
        with open(self.file, "a") as F: json.dump(json_data, F, ensure_ascii=False, indent=2)


def ReadConfiurations(C:list or dict):    
    if type(C) == dict:
        return C
    elif type(C) == str:
        with open(C, "r") as F: config = yaml.safe_load(F); F.close()
        return config
    
    
class Initialization:
    def __init__(self) -> None:
        pass

    def Set_Seed(self, random_seed:int=5943728):
        torch.manual_seed(random_seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
        numpy.random.seed(random_seed)
        random.seed(random_seed)
    
    def Set_device(self, gpu_id:str):
        return torch.device(f"cuda:{gpu_id}")
    
    
        
class Selector:
    def __init__(self) -> None:
        pass
    
    def Dataset(self, task: str, dataset_name:str, configurations:dict):
        if task == "Speaker Verification":
            return SpeakerVerification(dataset_name=dataset_name,
                                       configurations=configurations)
    
    def Architectures(self, architecture_name:str, configurations:dict):
        if architecture_name == "ECAPA-TDNN":
            return ECAPA_TDNN(**configurations)


    def Criterions(self, criterion_name:str, configurations:dict):
        if criterion_name == "AAMSoftmax":
            return AAM_Softmax(**configurations)
        
            
    def Optimizers(self, optimizer_name:str, trainable_parameters:Any, configrations:dict):
        if optimizer_name == "Adam":
            return Adam(params=trainable_parameters, **configrations)
        
        
class Timer:
    def __init__(self) -> None:
        self.start_time = None

    def Start(self,):
        self.start_time = time.time()
    
    def Stop(self):
        hours, remaining = divmod(time.time() - self.start_time, 3600)
        minutes, seconds = divmod(remaining, 60)
        o = "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds).split(".")[0]
        self.start_time = None
        return o
    
class Parameters:
    def __init__(self) -> None:
        pass
    
    def average_parameters(self, epoch, path):
        if epoch == 1:
            return None, None, None
        else:
            state_dict_paths = [i for i in path if f"temp_data_epoch{epoch-1}" in i]
            asd = {"a_{i}": torch.load(state_dict_paths[i]) for i in range(len(state_dict_paths))}
            csd = {"c_{i}": torch.load(state_dict_paths[i]) for i in range(len(state_dict_paths))}
            osd = {f"o_{i}": torch.load(state_dict_paths[i]) for i in range(len(state_dict_paths))}

            new_a = deepcopy(asd[list(asd.keys())[0]])
            new_c = deepcopy(csd[list(csd.keys())[0]])
            new_o = deepcopy(osd[list(osd.keys())[0]])
            
            a_keys = asd[list(asd.keys())[0]].keys()
            c_keys = csd[list(csd.keys())[0]].keys()
            o_keys = osd[list(osd.keys())[0]].keys()
            
            for i in a_keys:
                TEMP = []
                for j in asd.keys():            
                    TEMP.append(asd[j][i])
                if "num_batches_tracked" in i:
                    new_a[i] = asd[j][i]
                else:
                    new_a[i] = torch.stack(TEMP).mean(0)

            for j in c_keys:
                TEMP = []
                for j in asd.keys():            
                    TEMP.append(asd[j][i])
                if "num_batches_tracked" in i:
                    new_c[i] = asd[j][i]
                else:
                    new_c[i] = torch.stack(TEMP).mean(0)

            for l in state_dict_paths:
                subprocess.run([
                    "rm", "-rf", l
                ])

            return new_a, new_c, new_o
        
class DataSplits:
    def __init__(self) -> None:
        pass
    
    def random_split(self, dataset, num_splits):
        sizes = [math.floor(len(dataset)/num_splits) for _ in range(num_splits)]
        return torch.utils.data.random_split(dataset, sizes)