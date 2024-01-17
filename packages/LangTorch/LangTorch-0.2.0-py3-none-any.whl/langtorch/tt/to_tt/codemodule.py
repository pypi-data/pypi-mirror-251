from .textmodule import TextModule
from ...tensors import CodeTensor
from typing import Union, Callable


class CodeModule(TextModule):
    def __init__(self,
                 prompt: Union[str, 'TextTensor', Callable] = [""],
                 activation=None,
                 key=None,
                 memoize=False, *args, **kwargs):
        super().__init__(prompt, activation, key, memoize, *args, **kwargs)
        if not isinstance(prompt, CodeTensor):
            raise ValueError("Expected a CodeTensor for initialization.")

    def forward(self, input_text_tensor):
        return self._prompt.eval(input_text_tensor)