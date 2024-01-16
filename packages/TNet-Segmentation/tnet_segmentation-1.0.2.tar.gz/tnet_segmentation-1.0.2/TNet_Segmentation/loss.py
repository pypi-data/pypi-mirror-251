import torch.nn.functional as F
import torch.nn as nn


class DiceLoss(nn.Module):
    def __init__(self, smooth=1):
        super(DiceLoss, self).__init__()
        self.smooth = smooth

    def forward(self, predictions, targets):
        # Flatten predictions and targets
        predictions = predictions.view(predictions.size(0), -1)
        targets = targets.view(targets.size(0), -1)
        
        intersection = (predictions * targets).sum(dim=1)
        dice_coefficient = (2.0 * intersection + self.smooth) / (predictions.sum(dim=1) + targets.sum(dim=1) + self.smooth)

        dice_loss = 1 - dice_coefficient
        return dice_loss.mean()
