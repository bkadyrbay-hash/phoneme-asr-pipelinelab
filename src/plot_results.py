import argparse, glob, json, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--metrics_dir', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    metric_files = sorted(glob.glob(os.path.join(args.metrics_dir, '**', '*.json'), recursive=True))
    data = {}
    for mf in metric_files:
        with open(mf) as f: m = json.load(f)
        data.setdefault(m['lang'], {})[m['snr_db']] = m['mean_per']
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['#2196F3', '#E91E63', '#4CAF50']
    all_pers_by_snr = {}
    for idx, lang in enumerate(sorted(data.keys())):
        snrs = sorted(data[lang].keys())
        pers = [data[lang][s] for s in snrs]
        ax.plot(snrs, pers, marker='o', label=lang.upper(), color=colors[idx], linewidth=2)
        for snr, per in zip(snrs, pers):
            all_pers_by_snr.setdefault(snr, []).append(per)
    mean_snrs = sorted(all_pers_by_snr.keys())
    mean_pers = [sum(all_pers_by_snr[s])/len(all_pers_by_snr[s]) for s in mean_snrs]
    ax.plot(mean_snrs, mean_pers, marker='s', label='MEAN', color='black', linewidth=2.5, linestyle='--')
    ax.set_xlabel('SNR (dB)', fontsize=13)
    ax.set_ylabel('PER', fontsize=13)
    ax.set_title('ASR Robustness to Noise: PER vs SNR', fontsize=15)
    ax.legend(); ax.grid(True, alpha=0.3); ax.invert_xaxis()
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    plt.tight_layout()
    plt.savefig(args.output, dpi=150)

if __name__ == '__main__': main()
