import torch
import torch.nn as nn
from math import pow

class QuickDraw(nn.Module):
    def __init__(self, input_size = 28, num_classes = 200):
        super(QuickDraw, self).__init__()
        self.num_classes = num_classes
        # First convolution layer
        self.conv1 = nn.Sequential(nn.Conv2d(1, 32, 5, bias=False), 
                                   # Convert 1-channel grayscale image to 32 filters of 5x5
                                   nn.BatchNorm2d(32), 
                                   # Batch normalization - improves model learning speed and performance
                                   nn.ReLU(inplace=True),
                                   # Apply ReLU activation function
                                   nn.MaxPool2d(2,2))
                                   # 2x2 max pooling to halve the size of the feature map
        # Second convolution layer
        self.conv2 = nn.Sequential(nn.Conv2d(32, 64, 5, bias=False),
                                   # Convert 32 input channels to 64 filters of 5x5
                                   nn.BatchNorm2d(64),
                                   # Batch normalization
                                   nn.ReLU(inplace=True), 
                                   # Apply ReLU activation function
                                   nn.MaxPool2d(2, 2))
                                   # 2x2 max pooling to halve the size of the feature map
                                   
        dimension = int(64 * pow(input_size/4 - 3, 2))
        # Calculate the input dimension for the fully connected layer
        
        # First fully connected layer
        self.fc1 = nn.Sequential(nn.Linear(dimension, 512), 
                                 # Fully connected layer with 512 output neurons
                                 nn.BatchNorm1d(512),
                                 # Apply batch normalization
                                 nn.Dropout(0.5))
                                 # Apply dropout for regularization to prevent overfitting
        # Second fully connected layer
        self.fc2 = nn.Sequential(nn.Linear(512, 128), 
                                 # Fully connected layer with 128 output neurons
                                 nn.BatchNorm1d(128),
                                 # Batch normalization
                                 nn.Dropout(0.5))
                                 # Apply dropout to prevent overfitting
        # Output layer
        self.fc3 = nn.Sequential(nn.Linear(128, num_classes))
        # Set the number of output neurons according to the number of classes for classification

    def forward(self, input):
        output = self.conv1(input)
        output = self.conv2(output)
        output = output.view(output.size(0), -1)
        output = self.fc1(output)
        output = self.fc2(output)
        output = self.fc3(output)
        return output
