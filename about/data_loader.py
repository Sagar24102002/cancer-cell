import os
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms


class ImageCSVLoader(Dataset):
    """Dataset reading image paths and binary labels from a CSV file.

    CSV format: filepath,label  (label: 0 or 1)
    """

    def __init__(self, csv_df, transform=None):
        # csv_df: pandas.DataFrame with columns ['filepath','label']
        self.samples = csv_df.reset_index(drop=True)
        self.transform = transform or transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
        ])

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        row = self.samples.iloc[idx]
        path = row['filepath']
        label = int(row['label'])
        img = Image.open(path).convert('RGB')
        img = self.transform(img)
        return img, label
