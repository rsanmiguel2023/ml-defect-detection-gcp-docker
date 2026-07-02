"""
PyTorch ResNet18 model definition.
"""

import torch.nn as nn
from torchvision import models


def build_resnet18_model(num_classes: int):
    """
    Build a ResNet18 transfer learning model.
    """

    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)

    for parameter in model.parameters():
        parameter.requires_grad = False

    model.fc = nn.Linear(model.fc.in_features, num_classes)

    return model
