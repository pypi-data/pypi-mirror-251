from refyre.utils import optional_dependencies 

with optional_dependencies("warn"):
    import torch
    from torch.utils.data import Dataset

    class TorchStack(Dataset):
        def __init__(self, association, processor = lambda x : x):
            self.association = association
            self.processor = processor

            print('assoc', self.association)
            print('len', len(self.association))

        def __len__(self):
            return len(self.association)

        def items(self, k):
            '''
                If you are inheriting this dataset to make your own, 
                use this method to retrieve the data for the __getitem__ method
            '''
            return self.processor(*self.association[k].item())

        def __getitem__(self, idx):
            return self.items(idx)
