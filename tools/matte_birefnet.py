import torch, time, sys, os
from transformers import AutoModelForImageSegmentation
from PIL import Image
import av
from torchvision import transforms
src, out_dir = sys.argv[1], sys.argv[2]
os.makedirs(out_dir, exist_ok=True)
model = AutoModelForImageSegmentation.from_pretrained('ZhengPeng7/BiRefNet-portrait', trust_remote_code=True)
dev = 'mps'
model.to(dev).eval().half()
tf = transforms.Compose([transforms.Resize((1024, 1024)), transforms.ToTensor(), transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])
c = av.open(src); t0 = time.time(); n = 0
with torch.no_grad():
    for i, fr in enumerate(c.decode(video=0)):
        p = f'{out_dir}/f_{i:04d}.png'
        if os.path.exists(p):
            n += 1; continue
        im = fr.to_image().convert('RGB')
        x = tf(im).unsqueeze(0).to(dev).half()
        pred = model(x)[-1].sigmoid().float().cpu()[0, 0]
        mask = transforms.ToPILImage()(pred).resize(im.size, Image.BILINEAR)
        out = im.copy(); out.putalpha(mask); out.save(p); n += 1
        if i % 20 == 0:
            print(f'frame {i} {time.time()-t0:.0f}s', flush=True)
print(f'done {n} frames in {time.time()-t0:.0f}s', flush=True)
