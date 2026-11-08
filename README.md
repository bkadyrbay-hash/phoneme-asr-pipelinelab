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

## Known issue

The stored error rates should not be read as phoneme error rates. They are around 3.6 on clean audio, and a real PER should not behave like that. `evaluate.py` applies `jiwer.wer` to phoneme strings, which counts space-separated units, so the most likely cause is that references and predictions are split differently. The rate then falls to 1.0 at the lowest SNR levels, consistent with empty output. Scoring per phoneme is the fix, and the results need recomputing.

The noise seed also uses Python's `hash()`, which changes between runs unless `PYTHONHASHSEED` is set.
