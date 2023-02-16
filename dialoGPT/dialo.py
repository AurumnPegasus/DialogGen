from transformers import AutoTokenizer, AutoModelWithLMHead
from datasets import load_dataset
from icecream import ic
from loader import DataSet
import torch

dataset = load_dataset("bavard/personachat_truecased")



# ic(dataset['train'][0])

# the dataset has context and candidate sentences as lists of strings
# dialoGPT expects context and response so might need to create multiple training samples from each data sample
# one training sample per candidate sentence
# or should it be one training sample for the chosen response (indicated by later contexts)
# also seems that the chosen response is the last candidate sentence

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
tokenizer.add_special_tokens({'pad_token': '[PAD]'})
model = AutoModelWithLMHead.from_pretrained("microsoft/DialoGPT-small")

train_dataset = DataSet(dataset['train'], tokenizer)
val_dataset = DataSet(dataset['validation'], tokenizer)

train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=32, num_workers=2, shuffle=True)

for sample in train_loader:
    ic(type(sample['content']))
    print(sample['content'])
    break