import os, torch, random
from torch import nn, optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
from tqdm import tqdm
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

def safe_loader(path):
    try:
        with Image.open(path) as img:
            return img.convert("RGB")
    except Exception as e:
        print(f"[⚠️ Skipped corrupted image]: {path} ({e})")
        return Image.new("RGB", (224, 224))

def main():
    DATA_DIR = r"C:\Users\Sangam\AI_RealImage_Detector\data_unified"
    MODEL_DIR = r"C:\Users\Sangam\AI_RealImage_Detector\models"
    os.makedirs(MODEL_DIR, exist_ok=True)

    MODEL_PATH = os.path.join(MODEL_DIR, "ai_real_unified_strong.pth")
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    BATCH_SIZE = 24
    EPOCHS = 20
    LR = 5e-5

    # Strong augmentations
    train_tfms = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.RandomResizedCrop(224, scale=(0.7, 1.0)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(25),
        transforms.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.3, hue=0.05),
        transforms.RandomGrayscale(p=0.1),
        transforms.GaussianBlur(kernel_size=(3, 3), sigma=(0.1, 1.0)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225])
    ])

    val_tfms = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225])
    ])

    train_ds = datasets.ImageFolder(os.path.join(DATA_DIR, "train"), transform=train_tfms, loader=safe_loader)
    val_ds = datasets.ImageFolder(os.path.join(DATA_DIR, "val"), transform=val_tfms, loader=safe_loader)

    train_ld = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True, num_workers=4, pin_memory=True)
    val_ld = DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False, num_workers=4, pin_memory=True)

    print(f"✅ Loaded: {len(train_ds)} train, {len(val_ds)} val")

    # Model with dropout
    model = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.IMAGENET1K_V1)
    in_features = model.classifier[1].in_features
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.4),
        nn.Linear(in_features, 2)
    )
    model = model.to(DEVICE)

    # Label smoothing
    criterion = nn.CrossEntropyLoss(label_smoothing=0.1)
    optimizer = optim.AdamW(model.parameters(), lr=LR, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.OneCycleLR(optimizer, max_lr=LR,
                                              epochs=EPOCHS,
                                              steps_per_epoch=len(train_ld))
    scaler = torch.cuda.amp.GradScaler()

    best_acc = 0
    for epoch in range(EPOCHS):
        model.train()
        train_loss, correct, total = 0, 0, 0
        for x, y in tqdm(train_ld, desc=f"Epoch {epoch+1}/{EPOCHS} [Train]"):
            x, y = x.to(DEVICE), y.to(DEVICE)
            optimizer.zero_grad()
            with torch.cuda.amp.autocast():
                out = model(x)
                loss = criterion(out, y)
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
            scheduler.step()

            train_loss += loss.item() * x.size(0)
            _, preds = out.max(1)
            total += y.size(0)
            correct += preds.eq(y).sum().item()

        train_acc = correct / total
        train_loss /= total

        model.eval()
        val_loss, val_correct, val_total = 0, 0, 0
        with torch.no_grad(), torch.cuda.amp.autocast():
            for x, y in tqdm(val_ld, desc=f"Epoch {epoch+1}/{EPOCHS} [Val]"):
                x, y = x.to(DEVICE), y.to(DEVICE)
                out = model(x)
                loss = criterion(out, y)
                val_loss += loss.item() * x.size(0)
                _, preds = out.max(1)
                val_total += y.size(0)
                val_correct += preds.eq(y).sum().item()

        val_acc = val_correct / val_total
        val_loss /= val_total

        print(f"Epoch {epoch+1:02d}/{EPOCHS} | "
              f"train_acc={train_acc:.3f} val_acc={val_acc:.3f} | "
              f"train_loss={train_loss:.4f} val_loss={val_loss:.4f}")

        # Save every epoch
        torch.save({'model': model.state_dict(), 'acc': val_acc},
                   MODEL_PATH)

        if val_acc > best_acc:
            best_acc = val_acc
            torch.save({'model': model.state_dict()},
                       os.path.join(MODEL_DIR, "ai_real_unified_best_strong.pth"))
            print(f"✅ Saved new best model: val_acc={best_acc:.3f}")

    print(f"\n🏁 Done. Best validation accuracy: {best_acc:.3f}")

if __name__ == "__main__":
    main()
