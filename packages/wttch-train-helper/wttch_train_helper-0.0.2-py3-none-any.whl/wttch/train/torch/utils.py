import torch


def try_gpu() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "mps" if torch.mps else "cpu")
