import argparse, torch, os
import torch.multiprocessing as mp
from QUANTAVE.Paradigms.SpeakerVerification import TrainingObject, Timer, DataSplits, Parameters, Round, Graphs


P = argparse.ArgumentParser()
P.add_argument("YAMLPath", type=str)
A = P.parse_args()

OBJECTS = TrainingObject(configurations=A.YAMLPath)

if __name__ == "__main__":
        
    E = OBJECTS.load_trained_checkpoints()
    epoch_timer = Timer()
    
    
    train_data_splits = DataSplits().random_split(dataset=OBJECTS.dataset,
                                                  num_splits=OBJECTS.number_gpus)
    
    for epoch in range(E, OBJECTS.config["Training"]["Epochs"]+1):
        epoch_timer.Start()
        
        # Load state_dict
        SD = Parameters().average_parameters(E, OBJECTS.chalkboard.checkpoint_path)
        
        #------------------------------------------------------------------------#
        parent_processes = []
        for rank in range(OBJECTS.number_gpus):
            child_process = mp.Process(
                target=OBJECTS.train_epoch(data_split=train_data_splits[rank],
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
        # if epoch%OBJECTS.config["Evaluation"]["Calulate_After_Epochs"] == 0:
        #     evaluation_results = OBJECTS.evaluate(device=torch.device("cuda:0"))
        # else: evaluation_results = "Not calculated for this epoch"
        
        train_time = epoch_timer.Stop()    
        OBJECTS.chalkboard.scribe(
            "Epoch - {}, Loss - {}, {} - {}, Training Time - {}".format(
            epoch,
            Round(OBJECTS.EpochLoss),
            OBJECTS.config["Training"]["Training_Metric"],
            Round(OBJECTS.EpochMetric),
            train_time,
        ),
        evaluation_results
        )
        
        Graphs().LineGraph(data=OBJECTS.GraphLoss, title="Loss Graph", x_axis="Epochs", y_axis="Loss Value", line_label="Loss", line_color="#b83535",
                        save_image_path=os.path.join(OBJECTS.chalkboard.details_path, "Loss.png"))
        Graphs().LineGraph(data=OBJECTS.GraphMetric, title=OBJECTS.config["Training"]["Training_Metric"]+" Graph", x_axis="Epochs", line_color="#2335a8",
                        y_axis=OBJECTS.config["Training"]["Training_Metric"]+ " Graph", line_label=OBJECTS.config["Training"]["Training_Metric"],
                        save_image_path=os.path.join(OBJECTS.chalkboard.details_path, OBJECTS.config["Training"]["Training_Metric"]+".png"))
        torch.save(
            {
                "Epoch": epoch,
                "Architecture": OBJECTS.architecture.state_dict(),
                # "Criterion": OBJECTS.criterion.state_dict(),
                # "Optimizer": OBJECTS.optimizer.state_dict(),
            },
            f=OBJECTS.chalkboard.checkpoint_path + f"/Epoch_{epoch}.pth"
        )
        