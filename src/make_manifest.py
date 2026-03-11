import argparse, hashlib, json, os
from phonemizer import phonemize
import soundfile as sf

ESPEAK_LANG_MAP = {'en': 'en-us', 'fr': 'fr-fr'}

def md5_file(path):
    h = hashlib.md5()
    with open(path, 'rb') as f: h.update(f.read())
    return h.hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lang', required=True)
    parser.add_argument('--raw_dir', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    wav_dir = os.path.join(args.raw_dir, args.lang, 'wav')
    wav_files = sorted(f for f in os.listdir(wav_dir) if f.endswith('.wav'))
    records = []
    for wav_file in wav_files:
        wav_path = os.path.join(wav_dir, wav_file)
        stem = os.path.splitext(wav_file)[0]
        txt_path = wav_path.replace('.wav', '.txt')
        ref_text = open(txt_path).read().strip() if os.path.exists(txt_path) else stem
        ref_phon = phonemize(ref_text, language=ESPEAK_LANG_MAP.get(args.lang, 'en-us'), backend='espeak', with_stress=False).strip()
        info = sf.info(wav_path)
        records.append({'utt_id': f"{args.lang}_{stem}", 'lang': args.lang, 'wav_path': wav_path,
            'ref_text': ref_text, 'ref_phon': ref_phon, 'sr': info.samplerate,
            'duration_s': round(info.duration, 3), 'snr_db': None, 'audio_md5': md5_file(wav_path)})
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    tmp = args.output + '.tmp'
    with open(tmp, 'w') as f:
        f.write('\n'.join(json.dumps(r, ensure_ascii=False) for r in records) + '\n')
    os.replace(tmp, args.output)
    print(f'Manifest saved: {args.output}')

if __name__ == '__main__': main()
