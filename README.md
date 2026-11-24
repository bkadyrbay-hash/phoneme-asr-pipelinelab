# How does noise affect phoneme recognition in English and French?

A reproducible DVC-style pipeline that adds Gaussian noise to speech at 10 levels (40 dB to -15 dB SNR), transcribes it to phonemes with `facebook/wav2vec2-lv-60-espeak-cv-ft`, and scores the output against phonemized references. It runs on 50 utterances per language.

| Script | What it does |
|---|---|
| `src/make_manifest.py` | Builds a manifest and reference phonemes with espeak |
| `src/add_noise.py` | Adds noise at a given SNR |
| `src/run_inference.py` | Runs the wav2vec2 phoneme model |
| `src/evaluate.py` | Computes the error rate per language and noise level |
| `src/plot_results.py` | Draws the error rate against SNR |

Parameters are in `params.yaml`, per-level metrics in `results/metrics/`, the plot in `results/figures/per_vs_snr.png`. Audio is tracked with DVC and is not in this repository.

## Scoring

The error rate is computed over IPA symbols with spaces removed (`src/evaluate.py`). An earlier version applied WER to the phoneme strings; espeak separates words with spaces while the model separates phonemes, so that number was not a phoneme error rate. Results from that version were removed: run the pipeline again to regenerate `results/`.

Noise is seeded per utterance from a stable hash of its id, so runs are reproducible.

## Run it

```bash
pip install -r requirements.txt
# put the audio and manifests where params.yaml points, then run the scripts in the order above
```
