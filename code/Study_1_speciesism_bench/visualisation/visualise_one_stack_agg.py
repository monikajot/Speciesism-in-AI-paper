import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ..src.constants import model_mapping, model_files


def aggregate_model_runs(files, model_name, name="model_results_no_nans/"):
    """Aggregate data from three runs of a model and calculate means and stds"""
    run_results = []

    for file in files:
        try:
            df = pd.read_csv(f"{name}/{file}")
        except:
            try:
                df = pd.read_csv(f"model_results/{file}")
            except:
                continue

        # Get counts for this run
        print(file)
        grouped = df[[AGG_COLUMN, f'{model_name}_is_wrong_answer']].value_counts().unstack(fill_value=0)
        run_results.append(grouped[["wrong", "acceptable"]])

    if run_results:
        # Stack all runs
        all_runs = pd.concat(run_results)

        # Calculate means and stds by animal
        means = all_runs.groupby(level=0).mean()
        stds = all_runs.groupby(level=0).std()

        return means, stds
    return None, None


def visualise_animals_subplots(
        categories,
        model_data,
        figsize=(10, 25)):
    """
    Create subplot for each animal showing model comparisons
    """
    # Calculate number of rows needed (2 columns)
    n_rows = (len(categories) + 1) // 2

    fig, axes = plt.subplots(n_rows, 2, figsize=figsize)
    axes = axes.flatten()  # Make it easier to iterate over axes

    colors = {'acceptable': '#DCDCDC',
            'wrong': 'peru'}
    bar_width = 0.8

    # For each animal (subplot)
    for idx, animal in enumerate(categories):
        ax = axes[idx]
        x = np.arange(len(model_data))  # One position for each model

        acceptable_means = []
        acceptable_stds = []
        wrong_means = []
        wrong_stds = []
        model_names = []

        # Collect data for this animal across all models
        for model_name, (means, stds) in model_data.items():
            if animal in means.index:
                total = means.loc[animal, 'acceptable'] + means.loc[animal, 'wrong']

                # Calculate percentages
                acceptable_pct = (means.loc[animal, 'acceptable'] / total * 100)
                wrong_pct = (means.loc[animal, 'wrong'] / total * 100)

                # Calculate percentage standard deviations
                acceptable_std_pct = (stds.loc[animal, 'acceptable'] / total * 100)
                wrong_std_pct = (stds.loc[animal, 'wrong'] / total * 100)

                acceptable_means.append(acceptable_pct)
                acceptable_stds.append(acceptable_std_pct)
                wrong_means.append(wrong_pct)
                wrong_stds.append(wrong_std_pct)
                model_name = model_mapping[model_name] if model_name in model_mapping.keys() else model_name
                model_names.append(model_name)

        # Plot stacked bars
        print(animal, np.median(wrong_means), np.mean(wrong_stds))

        ax.bar(x, wrong_means, bar_width,
               color=colors['wrong'],
               label='Morally Wrong',
               yerr=wrong_stds,
               capsize=3)

        ax.bar(x, acceptable_means, bar_width,
               bottom=wrong_means,
               color=colors['acceptable'],
               label='Morally Acceptable',
               yerr=acceptable_stds,
               capsize=3)
        ax.axhline(y=np.mean(wrong_means), color='r', linestyle='--')
        ax.text(
            0.95, np.mean(wrong_means),  # x, y in data coordinates
            f"Mean = {np.mean(wrong_means):.2f}",
            color='r',
            va='bottom', ha='right',
            fontsize=10,
            fontweight='bold',
            backgroundcolor='white',
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.5),
            transform=ax.get_yaxis_transform()  # y in data, x in axes fraction
        )
        # ax.axhline(y=np.median(wrong_means), color='b', linestyle='-')

        # Styling
        ax.set_title(f'{animal.replace("_", " ").title()}', fontweight='bold')
        ax.set_ylabel('Percentage')
        ax.set_ylim(0, 100)
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.set_xticks(x)
        ax.set_xticklabels(model_names, rotation=45, ha='right')

        # Only show legend for first subplot
        if idx == 0:
            ax.legend()

    # Remove any empty subplots
    for idx in range(len(categories), len(axes)):
        fig.delaxes(axes[idx])

    # plt.suptitle(, fontsize=16, fontweight='bold')
    plt.tight_layout()
    return fig


if __name__ == "__main__":
    # Specify the animals we want to analyze
    AGG_COLUMN =  'speciesism_type'  #'animal' #
    top_animals = ['fish', 'rabbit', 'horse', 'chicken', 'sheep', 'pig', ]
    top_species = ['meat_animals', 'hunting_animals', 'fur_animals', 'leather_animals',  ]
    model_results = {}
    group_by = top_species

    # Process models in groups of 3 (for the runs)
    for i in range(0, len(model_files), 3):
        model_files_group = model_files[i:i + 3]
        model_name = model_files_group[0][1]  # Get model name from first file

        # Aggregate data from three runs
        means, stds = aggregate_model_runs(
            [f[0] for f in model_files_group],
            model_name
        )

        if means is not None:
            # Filter for only top animals
            means = means[means.index.isin(group_by)]
            stds = stds[stds.index.isin(group_by)]
            model_results[model_name] = (means, stds)
    # print(model_results)

    df = pd.DataFrame([
        {'model_name': model_name, 'means': means, 'stds': stds}
        for model_name, (means, stds) in model_results.items()
    ])
    print(df)
    # Create visualization
    fig = visualise_animals_subplots(
        categories=group_by,
        model_data=model_results,
        figsize=(16, 10)
    )

    # plt.show()
    plt.savefig('animal_model_comparison.svg', dpi=300, bbox_inches='tight')
