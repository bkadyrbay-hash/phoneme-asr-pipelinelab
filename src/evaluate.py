import argparse, json, os
from jiwer import wer

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--predictions', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    with open(args.predictions) as f:
        records = list(map(lambda l: json.loads(l.strip()), f.readlines()))
    refs = list(map(lambda r: r['ref_phon'], records))
    preds = list(map(lambda r: r['pred_phon'], records))
    per = wer(refs, preds)
    first = records[0]
    result = {'lang': first['lang'], 'snr_db': first['snr_db'], 'mean_per': round(per, 4), 'n_utterances': len(records)}
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'w') as f:
        json.dump(result, f, indent=2)

if __name__ == '__main__': main()
