import os
import torch


def save_checkpoint(state, out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    torch.save(state, out_path)


def makedir(path):
    os.makedirs(path, exist_ok=True)
