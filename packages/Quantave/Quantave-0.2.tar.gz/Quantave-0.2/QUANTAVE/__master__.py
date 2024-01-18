import argparse, os, yaml
from QUANTAVE.Paradigms.SpeakerVerification import TrainingObject


def proceed():
    P = argparse.ArgumentParser()
    P.add_argument("YAMLPath", type=str)
    A = P.parse_args()

    with open(A.YAMLPath, "r") as F: config = yaml.safe_load(F); F.close()

    if config["Training"]["Type"] == "SGPU":
        OBJECTS = TrainingObject(configurations=A.YAMLPath)
        OBJECTS.SGPU()

    if config["Training"]["Type"] == "MGPU":
        _gpu_path = "/".join(__file__.split("/")[:-1])+"/Paradigms/__SpeakerVerification_MGPU__.py"
        os.system(" ".join(["python3",
                            _gpu_path,
                            A.YAMLPath]))
    else:
        print("Training Type must be MGPU or SGPU")
    

if __name__ == "__main__":
    proceed()