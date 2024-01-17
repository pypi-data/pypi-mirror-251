"""Semantic Algebra Functional interface"""
from typing import List, Optional, Union
import langtorch

from .session import Session
import numpy as np
import torch

TextTensor = langtorch.TextTensor
Text = langtorch.Text
set_defaults_from_ctx = langtorch.decorators.set_defaults_from_ctx
@set_defaults_from_ctx
def mean(input: TextTensor,
         method="""We have a set of text entries, separated by '---'.
Your task is to create the average of these texts. By an average text we mean a text that is as short as one entry, but incorporates information from all the entries written in a similar style.
Answer only with the short text that averages these texts:\n\n""",
         dim: Optional[Union[int, List[int]]] = None, keepdim: bool = False, dtype: Optional = Text,
         model='default') -> TextTensor:
    input = input.join("\n---\n", dim=dim)
    if keepdim:
        input = input.unsqueeze(dim)
    input = TextTensor(method) * input
    if model == 'default':
        output = langtorch.tt.Activation('gpt3.5-turbo')(input)
    else:
        output = langtorch.tt.Activation(model=model)(input)
    return output

def stack(text_tensors, dim=0, *, out=None):
    # Validate the input tensors
    if not all(isinstance(t, TextTensor) for t in text_tensors):
        raise TypeError("All inputs must be TextTensor instances")

    # Stack the contents
    stacked_content = np.stack([t.content for t in text_tensors], axis=dim)

    # Merge the metadata
    merged_metadata = {}
    for key in text_tensors[0].metadata.keys():
        if isinstance(text_tensors[0].metadata[key], torch.Tensor):
            # For tensor-like metadata, stack them along the specified dimension
            merged_metadata[key] = torch.stack([t.metadata[key] for t in text_tensors], dim=dim)
        else:
            # For scalar or non-tensor metadata, use the metadata from the first tensor
            merged_metadata[key] = text_tensors[0].metadata[key]

    # Create a new TextTensor with the stacked content and merged metadata
    stacked_tensor = TextTensor(metadata=merged_metadata, content=stacked_content, parse=False)

    # Handle the 'out' argument if provided
    if out is not None:
        if not isinstance(out, TextTensor):
            raise TypeError("The 'out' argument must be a TextTensor instance")
        out.metadata = stacked_tensor.metadata
        out.content = stacked_tensor.content
        return out

    return stacked_tensor
