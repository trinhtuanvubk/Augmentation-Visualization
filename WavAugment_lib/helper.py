import torch

#  function to convert from float32 to int16
def SoundDataToInt(SD:torch.Tensor) :
    SD[0] = torch.Tensor([int(s*32768) for s in SD[0].tolist()])
    SD = SD.type(torch.int16)
    return SD