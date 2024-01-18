from .HelperTools import *
import torch.multiprocessing as mp
from torch.utils.data import DataLoader
from ..Functions.Visualization import Graphs
from ..Functions.EvaluationMetrics import EqualErrorRate
from ..Functions.TrainingMetrics import TrainingMetrics as TMetric



class TrainingObject:
    def __init__(self,
                 configurations:str or dict,
                 *args, **kwargs) -> None:

        self.config = ReadConfiurations(C=configurations)
        self.chalkboard = ChalkBoard(experiment_name=self.config["Experiment_Name"])
        self.mgpu = True if self.config["Training"]["Type"] == "MGPU" else False
        self.TrainCriterion = self.config["Training"].get("Train_Criterion", False)
        
        if not self.mgpu:
            self.device = Initialization().Set_device(gpu_id=self.config["Training"].get("GPU_ID", 0))

        # Functions Initializations
        
        if self.config["Dataset"]["Task"] != "Speaker Verification":
            raise Exception("This is Speaker Verification training paradigm.")
    
        self.dataset = Selector().Dataset(task=self.config["Dataset"]["Task"],
                                          dataset_name=self.config["Dataset"]["Name"],
                                          configurations=self.config["Dataset"]["Configurations"])
        
        if not self.mgpu:
            self.dataloader = DataLoader(dataset=self.dataset,
                                         batch_size=self.config["Training"]["Batch_Size"],
                                         shuffle=True,
                                         pin_memory=True,
                                         num_workers=self.config["Training"].get("Number_Workers", 8),
                                         drop_last=True)

        self.architecture = Selector().Architectures(architecture_name=self.config["Architecture"]["Name"],
                                                     configurations=self.config["Architecture"]["Configurations"])

        if not self.mgpu:        
            self.criterion = Selector().Criterions(criterion_name=self.config["Criterion"]["Name"],
                                                configurations=self.config["Criterion"]["Configurations"])
            
            self.optimizer = Selector().Optimizers(optimizer_name=self.config["Optimizer"]["Name"],
                                                trainable_parameters=self.parameter_selector(selection=self.TrainCriterion),
                                                configrations=self.config["Optimizer"]["Configurations"])
        
        if not self.mgpu:
            self.move_on_gpu(device=self.device)
            
        self.GraphLoss = []
        self.GraphMetric = []
        
        if self.mgpu: 
            if self.config["Training"]["MGPU_Configurations"]["nodes"] != 1:
                raise Exception("Implemented to run only on a single cluster Multi-GPU system")
            
            self.number_gpus = self.config["Training"]["MGPU_Configurations"]["nodes"]*self.config["Training"]["MGPU_Configurations"]["ngpus_per_node"]
            
            self.EpochLoss = [0 for _ in range(self.number_gpus)]
            self.EpochMetric = [0 for _ in range(self.number_gpus)]
        else:
            self.EpochLoss = 0
            self.EpochMetric = 0

    def parameter_selector(self, selection:bool, criterion=None):
        if self.mgpu:
            if selection:
                return list(self.architecture.parameters())+list(criterion.parameters())
            else:
                return self.architecture.parameters()
        else:            
            if selection:
                return list(self.architecture.parameters())+list(self.criterion.parameters())
            else:
                return self.architecture.parameters()

    def move_on_gpu(self,
                    device:torch.device):    
        self.architecture.to(device)
        self.criterion.to(device)
        
    def load_trained_checkpoints(self,):
        if self.config["Training"]["Resume_Training_Checkpoint_Path"] != "":
            data = torch.load(f=self.config["Training"]["Resume_Training_Checkpoint_Path"])
            
            self.architecture.load_state_dict(state_dict=data["Architecture"])
            self.criterion.load_state_dict(state_dict=data["Criterion"])
            self.optimizer.load_state_dict(state_dict=data["Optimizer"])
            return data["Epoch"]
        
        else: return 1
    
    def train_epoch(self, data_split, device, epoch, *args, **kwargs):        
        torch.autograd.set_detect_anomaly(True)
        
        self.architecture = self.architecture.to(device)
        self.architecture.train()
        
        if self.mgpu:
            self.EpochLoss = [0 for _ in range(self.number_gpus)]
            self.EpochMetric = [0 for _ in range(self.number_gpus)]
            
            if kwargs.get("architecture_param", None) != None:
                self.architecture.load_state_dict(kwargs.get("architecture_param", None))

            process = int(device.__str__().split(":")[-1])
            dataloader = DataLoader(dataset=data_split,
                                    batch_size=self.config["Training"]["Batch_Size"],
                                    shuffle=True,
                                    pin_memory=True,
                                    num_workers=self.config["Training"].get("Number_Workers", 8))
            total_minibatches = len(dataloader)
            
            criterion = Selector().Criterions(criterion_name=self.config["Criterion"]["Name"],
                                              configurations=self.config["Criterion"]["Configurations"])
            if kwargs.get("criterion_param", None) != None:
                criterion.load_state_dict(kwargs.get("criterion_param", None))
            
            if self.TrainCriterion:
                criterion = criterion.to(device)
                criterion.train()
            
            optimizer = Selector().Optimizers(optimizer_name=self.config["Optimizer"]["Name"],
                                              trainable_parameters=self.parameter_selector(selection=self.TrainCriterion, criterion=criterion),
                                              configrations=self.config["Optimizer"]["Configurations"])
            
            if kwargs.get("optimizer_param", None) != None:
                optimizer.load_state_dict(kwargs.get("optimizer_param", None))
        else:
            self.EpochLoss, self.EpochMetric = 0, 0
            total_minibatches = len(self.dataloader)
            
        for mb_idx, minibatch in enumerate(dataloader if self.mgpu else self.dataloader):
            
            mb_data, mb_labels = minibatch
            mb_data, mb_labels = mb_data.to(device), mb_labels.to(device)
            
            if self.mgpu:
                optimizer.zero_grad()
                logits = self.architecture(mb_data)
                loss, prediction = criterion(logits, mb_labels)
                loss.backward()
                optimizer.step()
                
                self.EpochLoss[process] += loss.item()
                metric = TMetric[self.config["Training"]["Training_Metric"]](
                    correct=mb_labels.eq(prediction.argmax(1)).sum(),
                    total=self.config["Training"]["Batch_Size"]
                )
                self.EpochMetric[process] += metric.item()
                
                if mb_idx % self.config["Training"]["Log_After_Minibatch"] == 0:
                    self.chalkboard.scribe(
                        "Process: {}, Epoch - {} :: {}/{}, Minibatch [Loss: {}, {}: {}]".format(
                            mp.current_process().name,
                            epoch,
                            mb_idx,
                            total_minibatches,
                            Round(loss.item()),
                            self.config["Training"]["Training_Metric"],
                            Round(metric)  
                        )
                    )
            else:
                self.optimizer.zero_grad()
                logits = self.architecture(mb_data, *args, **kwargs)
                loss, prediction = self.criterion(logits, mb_labels,*args, **kwargs)
                loss.backward()
                self.optimizer.step()
                
                self.EpochLoss += loss.item()
                metric = TMetric[self.config["Training"]["Training_Metric"]](
                    correct=mb_labels.eq(prediction.argmax(1)).sum(),
                    total=self.config["Training"]["Batch_Size"]
                )
                self.EpochMetric += metric.item()
                
                if mb_idx % self.config["Training"]["Log_After_Minibatch"] == 0:
                    self.chalkboard.scribe(
                        "Epoch - {} :: {}/{}, Minibatch [Loss: {}, {}: {}]".format(
                            epoch,
                            mb_idx,
                            total_minibatches,
                            Round(loss.item()),
                            self.config["Training"]["Training_Metric"],
                            Round(metric)  
                        )
                    )

        if self.mgpu:
            torch.save(obj={"a": self.architecture.state_dict(),
                            "c": criterion.state_dict(),
                            "o": optimizer.state_dict()
                            },
                       f=self.chalkboard.checkpoint_path+f"/temp_data__epoch_{epoch}_{process}.dat"
                       )
            
            self.EpochLoss = numpy.average(self.EpochLoss)/total_minibatches
            self.EpochMetric = numpy.average(self.EpochMetric)/total_minibatches
            self.GraphLoss.append(self.EpochLoss)
            self.GraphMetric.append(self.EpochMetric)
        else:
            self.GraphLoss.append(self.EpochLoss/total_minibatches)
            self.GraphMetric.append(self.EpochMetric/total_minibatches)
            self.EpochLoss = self.EpochLoss/total_minibatches
            self.EpochMetric = self.EpochMetric/total_minibatches
    
    def evaluate(self, device:torch.device or int):
        timer = Timer()
        
        if self.config["Dataset"]["Name"] == "voxceleb":
            pair_list = self.dataset.evaluation_pair_list
        
        if self.config["Evaluation"]["Metric"] == "EER":
            timer.Start()
                
            self.architecture.eval()
            
            eer, min_dcf = EqualErrorRate(forward_fn=self.architecture.forward,
                                          evaluation_pair_list=pair_list,
                                          device=device)
            evaluation_time = timer.Stop()
            return f"EER - {Round(eer)}, Min_DCF - {Round(min_dcf)}, Evaluation Time - {evaluation_time}"
        
        if self.config["Evaluation"]["Metric"] == "Accuracy":
            return "Not Implemented"
        
    def SGPU(self,):
        E = self.load_trained_checkpoints()
        epoch_timer = Timer()        

        for epoch in range(E, self.config["Training"]["Epochs"]+1):
            epoch_timer.Start()
            self.train_epoch(
                data_split=None,
                device=self.device,
                epoch=E,
            )
            
            if epoch%self.config["Evaluation"]["Calulate_After_Epochs"] == 0:
                evaluation_results = self.evaluate(device=self.device)
            else: evaluation_results = "Not calculated for this epoch"
            
            train_time = epoch_timer.Stop()    
            self.chalkboard.scribe(
                "Epoch - {}, Loss - {}, {} - {}, Training Time - {}".format(
                epoch,
                Round(self.EpochLoss),
                self.config["Training"]["Training_Metric"],
                Round(self.EpochMetric),
                train_time,
            ),
            evaluation_results
            )
            
            Graphs().LineGraph(data=self.GraphLoss, title="Loss Graph", x_axis="Epochs", y_axis="Loss Value", line_label="Loss", line_color="#b83535",
                            save_image_path=os.path.join(self.chalkboard.details_path, "Loss.png"))
            Graphs().LineGraph(data=self.GraphMetric, title=self.config["Training"]["Training_Metric"]+" Graph", x_axis="Epochs", line_color="#2335a8",
                            y_axis=self.config["Training"]["Training_Metric"]+ " Graph", line_label=self.config["Training"]["Training_Metric"],
                            save_image_path=os.path.join(self.chalkboard.details_path, self.config["Training"]["Training_Metric"]+".png"))
            torch.save(
                {
                    "Epoch": epoch,
                    "Architecture": self.architecture.state_dict(),
                    "Criterion": self.criterion.state_dict(),
                    "Optimizer": self.optimizer.state_dict(),
                },
                f=self.chalkboard.checkpoint_path + f"/Epoch_{epoch}.pth"
            )
            
    def MGPU(self,):
        if self.config["Training"]["MGPU_Configurations"]["nodes"] != 1:
            raise Exception("Implemented to run only on a single cluster Multi-GPU system")
        
        E = self.load_trained_checkpoints()
        epoch_timer = Timer()
        
        
        train_data_splits = DataSplits().random_split(dataset=self.dataset,
                                                      num_splits=self.number_gpus)
        
        
        
        for epoch in range(E, self.config["Training"]["Epochs"]+1):
            epoch_timer.Start()
            
            # Load state_dict
            SD = Parameters().average_parameters(E, self.chalkboard.checkpoint_path)
            
            #------------------------------------------------------------------------#
            parent_processes = []
            for rank in range(self.number_gpus):
                child_process = mp.Process(
                    target=self.train_epoch(data_split=train_data_splits[rank],
                                            device=torch.device(f"cuda:{rank}"),
                                            epoch=epoch,
                                            architecture_param=SD[0],
                                            criterion_param=SD[1],
                                            optimizer_param=SD[2]),
                    name=f"Child_Process-{rank}"
                )
                child_process.start()
                parent_processes.append(child_process)
            
            for childrens in parent_processes:
                childrens.join()
            #------------------------------------------------------------------------#
            
            #TODO: add multi-gpu evaluation code
            
            evaluation_results = "Yet to be implemented."
            # if epoch%self.config["Evaluation"]["Calulate_After_Epochs"] == 0:
            #     evaluation_results = self.evaluate(device=torch.device("cuda:0"))
            # else: evaluation_results = "Not calculated for this epoch"
            
            train_time = epoch_timer.Stop()    
            self.chalkboard.scribe(
                "Epoch - {}, Loss - {}, {} - {}, Training Time - {}".format(
                epoch,
                Round(self.EpochLoss),
                self.config["Training"]["Training_Metric"],
                Round(self.EpochMetric),
                train_time,
            ),
            evaluation_results
            )
            
            Graphs().LineGraph(data=self.GraphLoss, title="Loss Graph", x_axis="Epochs", y_axis="Loss Value", line_label="Loss", line_color="#b83535",
                            save_image_path=os.path.join(self.chalkboard.details_path, "Loss.png"))
            Graphs().LineGraph(data=self.GraphMetric, title=self.config["Training"]["Training_Metric"]+" Graph", x_axis="Epochs", line_color="#2335a8",
                            y_axis=self.config["Training"]["Training_Metric"]+ " Graph", line_label=self.config["Training"]["Training_Metric"],
                            save_image_path=os.path.join(self.chalkboard.details_path, self.config["Training"]["Training_Metric"]+".png"))
            torch.save(
                {
                    "Epoch": epoch,
                    "Architecture": self.architecture.state_dict(),
                    # "Criterion": self.criterion.state_dict(),
                    # "Optimizer": self.optimizer.state_dict(),
                },
                f=self.chalkboard.checkpoint_path + f"/Epoch_{epoch}.pth"
            )
            