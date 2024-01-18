import torch

        
def accuracy(correct:torch.Tensor, total:torch.Tensor or int, *args, **kwargs):
    return correct.div(total).mul(100)


TrainingMetrics = {
    "Accuracy": accuracy
}