from .textmodule import TextModule
from ...tensors import ChatTensor
import torch


class ChatModule(TextModule):
    tensor_class = ChatTensor