import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from ..src.constants import FINAL_RESULTS, model_mapping


def ubound(mu, std):
    l = []
    for i, val in enumerate(mu):
        x = 100-mu[i] if mu[i]+std[i] > 100 else std[i]
        l.append(x)
    return np.array(l)


def plot_with_stats(data):
    # Convert to DataFrame and group by model
    df = pd.DataFrame(data)
    stats = df.groupby('model', sort=False).agg(['mean', 'std']).fillna(0).round(2)
    print("STATS")
    print(stats)
    stats.to_csv("final_results_stats.csv")
    models = stats.index.tolist()
    models = [model_mapping[model]  if model in model_mapping.keys() else models for model in models ]

    # Extract means and stds
    wrong_mean = stats[('wrong', 'mean')].values
    wrong_std = stats[('wrong', 'std')].values
    not_wrong_mean = stats[('not wrong', 'mean')].values
    not_wrong_std = stats[('not wrong', 'std')].values
    speciesist_mean = stats[('speciesist', 'mean')].values
    speciesist_std = stats[('speciesist', 'std')].values
    not_speciesist_mean = stats[('not speciesist', 'mean')].values
    not_speciesist_std = stats[('not speciesist', 'std')].values

    # Plot setup
    bar_width = 0.35
    x = np.arange(len(models))
    fig, ax = plt.subplots(figsize=(16, 8))

    # Colors
    colors = {'wrong': 'peru', 'not wrong': '#DCDCDC',
              'speciesist': 'steelblue', 'not speciesist': 'silver'}


    b3 = ax.bar(x - bar_width / 2, speciesist_mean, bar_width, label='Speciesist',
                color=colors['speciesist'])
    b4 = ax.bar(x - bar_width / 2, not_speciesist_mean, bar_width, bottom=speciesist_mean,
                label='Not speciesist', color=colors['not speciesist'])
    b1 = ax.bar(x + bar_width / 2, wrong_mean, bar_width, label='Morally wrong', color=colors['wrong'])
    b2 = ax.bar(x + bar_width / 2, not_wrong_mean, bar_width, bottom=wrong_mean,
                label='Morally acceptable', color=colors['not wrong'])

    # Error bars
    total_left = wrong_mean + not_wrong_mean
    total_left_std = np.sqrt(wrong_std ** 2 + not_wrong_std ** 2)
    total_right = speciesist_mean + not_speciesist_mean

    ax.errorbar(x - bar_width / 2,speciesist_mean , yerr=speciesist_std, fmt='none',
                capsize=3, capthick=1, ecolor='black', alpha=0.8)
    ax.errorbar(x - bar_width / 2, total_right , yerr=[not_speciesist_std, ubound(total_right, not_speciesist_std)], fmt='none',
                capsize=3, capthick=1, ecolor='black', alpha=0.8)
    ax.errorbar(x + bar_width / 2, wrong_mean, yerr=wrong_std, fmt='none',
                capsize=3, capthick=1, ecolor='black', alpha=0.8)
    ax.errorbar(x + bar_width / 2, total_left, yerr=[not_wrong_std, ubound(total_left, not_wrong_std)], fmt='none',
                capsize=3, capthick=1, ecolor='black', alpha=0.8)


    # Labels and formatting
    ax.set_xlabel('Models', fontweight='bold')
    ax.set_ylabel('Answers (percentage)', fontweight='bold')
    ax.set_title('SpeciesismBench (Mean ± Std)', fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(models, rotation=45, ha='right')
    plt.legend(bbox_to_anchor=(0.5, -0.25), loc='upper center', ncol=4)

    ax.grid(True, linestyle='--', alpha=0.4)

    plt.tight_layout()
    plt.show()
    plt.savefig("figure_1.svg")

    return  ax

if __name__ == "__main__":

    normalised_data = []
    for d in FINAL_RESULTS:
        new_d = {}
        # den = sum([val for key, val in d.items() if type(val)==int])
        for k, v in d.items():
            if type(v) == int:
                new_d[k] = round(v * 100 / 1003, 2)
            else:
                new_d["model"] = v
        normalised_data.append(new_d)
    print(FINAL_RESULTS)
    print(normalised_data)
    pd.DataFrame(normalised_data).to_csv("final_results.csv")
    plot_with_stats(normalised_data)
