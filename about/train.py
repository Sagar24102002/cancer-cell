import argparse
import os
import time
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import transforms

from data_loader import ImageCSVLoader
from model import get_resnet18
from utils import save_checkpoint, makedir


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--train_csv', required=True)
    p.add_argument('--val_csv', required=True)
    p.add_argument('--output_dir', default='runs/exp')
    p.add_argument('--epochs', type=int, default=5)
    p.add_argument('--batch_size', type=int, default=16)
    p.add_argument('--lr', type=float, default=1e-4)
    p.add_argument('--device', default='cuda' if torch.cuda.is_available() else 'cpu')
    return p.parse_args()


def train(args):
    makedir(args.output_dir)

    train_df = pd.read_csv(args.train_csv)
    val_df = pd.read_csv(args.val_csv)

    train_trans = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
    ])
    val_trans = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])

    train_ds = ImageCSVLoader(train_df, transform=train_trans)
    val_ds = ImageCSVLoader(val_df, transform=val_trans)

    train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True, num_workers=2)
    val_loader = DataLoader(val_ds, batch_size=args.batch_size, shuffle=False, num_workers=2)

    model = get_resnet18(num_classes=2, pretrained=True)
    model = model.to(args.device)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)

    best_acc = 0.0
    for epoch in range(1, args.epochs + 1):
        model.train()
        running_loss = 0.0
        total = 0
        correct = 0
        for imgs, labels in train_loader:
            imgs = imgs.to(args.device)
            labels = labels.to(args.device)
            optimizer.zero_grad()
            outputs = model(imgs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item() * imgs.size(0)
            _, preds = outputs.max(1)
            total += labels.size(0)
            correct += (preds == labels).sum().item()

        train_loss = running_loss / total
        train_acc = correct / total

        # validation
        model.eval()
        total = 0
        correct = 0
        with torch.no_grad():
            for imgs, labels in val_loader:
                imgs = imgs.to(args.device)
                labels = labels.to(args.device)
                outputs = model(imgs)
                _, preds = outputs.max(1)
                total += labels.size(0)
                correct += (preds == labels).sum().item()

        val_acc = correct / total

        print(f"Epoch {epoch}/{args.epochs}  Train loss: {train_loss:.4f}  Train acc: {train_acc:.4f}  Val acc: {val_acc:.4f}")

        ckpt = {
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'val_acc': val_acc,
        }
        save_checkpoint(ckpt, os.path.join(args.output_dir, f'model_epoch{epoch}.pth'))
        if val_acc > best_acc:
            best_acc = val_acc
            save_checkpoint(ckpt, os.path.join(args.output_dir, 'model_best.pth'))


if __name__ == '__main__':
    args = parse_args()
    start = time.time()
    train(args)
    print('Done. Time:', time.time() - start)
