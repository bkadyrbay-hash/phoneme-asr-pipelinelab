"""Phoneme error rate for one language and noise level.

References come from espeak, which separates words with spaces; the wav2vec2
phoneme model separates phonemes with spaces. Counting space-separated units
(as WER does) therefore compares different things. Here both strings are
reduced to their IPA symbols with spaces removed and scored with an edit
distance over symbols, so the rate is comparable across utterances.
"""
import argparse
import json
import os
import unicodedata

import jiwer


def to_symbols(s: str) -> str:
    """Normalise IPA and drop all whitespace."""
    s = unicodedata.normalize("NFC", s)
    return "".join(s.split())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--predictions", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    with open(args.predictions, encoding="utf-8") as f:
        records = [json.loads(line) for line in f if line.strip()]

    refs = [to_symbols(r["ref_phon"]) for r in records]
    preds = [to_symbols(r["pred_phon"]) for r in records]
    per = jiwer.cer(refs, preds)

    result = {
        "lang": records[0]["lang"],
        "snr_db": records[0]["snr_db"],
        "per": round(per, 4),
        "n_utterances": len(records),
        "empty_predictions": sum(1 for p in preds if not p),
    }
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)


if __name__ == "__main__":
    main()
