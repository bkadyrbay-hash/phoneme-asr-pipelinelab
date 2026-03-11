import argparse, hashlib, json, os
import numpy as np
import soundfile as sf

def add_noise(signal, snr_db, rng):
    signal_power = np.mean(signal ** 2)
    snr_linear = 10 ** (snr_db / 10)
    noise_power = signal_power / snr_linear
    noise = rng.normal(loc=0.0, scale=np.sqrt(noise_power), size=signal.shape)
    return signal + noise

def add_noise_to_file(input_wav, output_wav, snr_db, seed=None):
    signal, sr = sf.read(input_wav)
    if signal.ndim != 1: raise ValueError('Only mono audio is supported')
    rng = np.random.default_rng(seed)
    sf.write(output_wav, add_noise(signal, snr_db, rng), sr)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--manifest', required=True)
    parser.add_argument('--snr_db', type=float, required=True)
    parser.add_argument('--output_dir', required=True)
    parser.add_argument('--output_manifest', required=True)
    parser.add_argument('--seed', type=int, default=42)
    args = parser.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    with open(args.manifest) as f:
        records = list(map(lambda l: json.loads(l.strip()), f.readlines()))
    snr_str = str(int(args.snr_db)).replace('-', 'neg')
    def process(rec):
        out_wav = os.path.join(args.output_dir, f"{rec['utt_id']}_snr{snr_str}.wav")
        add_noise_to_file(rec['wav_path'], out_wav, args.snr_db, seed=args.seed + abs(hash(rec['utt_id'])) % (2**31))
        return {**rec, 'wav_path': out_wav, 'snr_db': args.snr_db}
    noisy = list(map(process, records))
    tmp = args.output_manifest + '.tmp'
    with open(tmp, 'w') as f:
        f.write('\n'.join(json.dumps(r, ensure_ascii=False) for r in noisy) + '\n')
    os.replace(tmp, args.output_manifest)

if __name__ == '__main__': main()
