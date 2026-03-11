import argparse, json, os
import torch, soundfile as sf
import numpy as np
from transformers import AutoProcessor, AutoModelForCTC

MODEL_ID = 'facebook/wav2vec2-lv-60-espeak-cv-ft'
TARGET_SR = 16000

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--manifest', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    processor = AutoProcessor.from_pretrained(MODEL_ID)
    model = AutoModelForCTC.from_pretrained(MODEL_ID)
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = model.to(device).eval()
    with open(args.manifest) as f:
        records = list(map(lambda l: json.loads(l.strip()), f.readlines()))
    def transcribe(rec):
        signal, sr = sf.read(rec['wav_path'])
        signal = signal.astype(np.float32)
        inputs = processor(signal, sampling_rate=TARGET_SR, return_tensors='pt', padding=True)
        inputs = {k: v.to(device) for k, v in inputs.items()}
        with torch.no_grad():
            logits = model(**inputs).logits
        pred = processor.batch_decode(torch.argmax(logits, dim=-1))[0].strip()
        return {**rec, 'pred_phon': pred}
    results = list(map(transcribe, records))
    tmp = args.output + '.tmp'
    with open(tmp, 'w') as f:
        f.write('\n'.join(json.dumps(r, ensure_ascii=False) for r in results) + '\n')
    os.replace(tmp, args.output)

if __name__ == '__main__': main()
