import torch

class DataSet(torch.utils.data.Dataset):
    def __init__(self, data, tokenizer):
        self.data = data
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        candidate = self.data[idx]['candidates'][-1]
        history = self.data[idx]['history']

        cemb = self.tokenizer(candidate, truncation=True, padding='max_length')
        hemb = self.tokenizer(candidate, truncation=True, padding='max_length')

        

        return {'content': cemb, 'history': hemb}