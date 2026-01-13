import argparse
import pandas as pd
import torch
from torch.utils.data import DataLoader
from sklearn.metrics import accuracy_score, roc_auc_score
from torchvision import transforms

from data_loader import ImageCSVLoader
from model import get_resnet18


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--csv', required=True)
    p.add_argument('--checkpoint', required=True)
    p.add_argument('--batch_size', type=int, default=16)
    p.add_argument('--device', default='cuda' if torch.cuda.is_available() else 'cpu')
    p.add_argument('--out', default='predictions.csv')
    return p.parse_args()


def evaluate(args):
    df = pd.read_csv(args.csv)
    trans = transforms.Compose([transforms.Resize((224, 224)), transforms.ToTensor()])
    ds = ImageCSVLoader(df, transform=trans)
    loader = DataLoader(ds, batch_size=args.batch_size, shuffle=False, num_workers=2)

    model = get_resnet18(num_classes=2, pretrained=False)
    ckpt = torch.load(args.checkpoint, map_location=args.device)
    model.load_state_dict(ckpt['model_state_dict'])
    model = model.to(args.device)
    model.eval()

    ys = []
    y_probs = []
    with torch.no_grad():
        for imgs, labels in loader:
            imgs = imgs.to(args.device)
            outputs = model(imgs)
            probs = torch.softmax(outputs, dim=1)[:, 1].cpu().numpy()
            preds = outputs.argmax(1).cpu().numpy()
            ys.extend(labels.numpy().tolist())
            y_probs.extend(probs.tolist())

    acc = accuracy_score(ys, [int(p >= 0.5) for p in y_probs])
    try:
        auc = roc_auc_score(ys, y_probs)
    except Exception:
        auc = float('nan')

    print(f'Accuracy: {acc:.4f}  ROC AUC: {auc:.4f}')
    out_df = pd.DataFrame({'filepath': df['filepath'], 'label': df['label'], 'prob_malignant': y_probs})
    out_df.to_csv(args.out, index=False)


if __name__ == '__main__':
    args = parse_args()
    evaluate(args)
