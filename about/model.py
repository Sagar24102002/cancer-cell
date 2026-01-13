import torch
import torch.nn as nn
from torchvision import models


def get_resnet18(num_classes=2, pretrained=True):
    model = models.resnet18(pretrained=pretrained)
    in_features = model.fc.in_features
    model.fc = nn.Linear(in_features, num_classes)
    return model


def load_checkpoint(path, device='cpu'):
    state = torch.load(path, map_location=device)
    return state
