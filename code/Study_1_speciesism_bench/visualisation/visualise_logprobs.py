import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ..src.constants import model_mapping

name = "model_results/"
files =[ "gemini-1.5_results_0.csv"]
models = [ "gemini-1.5"]

def plot_logprob_distributions_hist_line(df, bins=50, figsize=(12, 8)):
    """
    Create line plots from histogram data for each model
    """
    logprobs ="morally acceptable logprobs"
    plt.figure(figsize=figsize)

    models = df['model'].unique()
    colors = plt.cm.Set1(np.linspace(0, 1, len(models)))

    for i, model in enumerate(models):
        model_data = df[df['model'] == model][logprobs]


        # Create histogram
        counts, bin_edges = np.histogram(model_data, bins=bins, density=True)

        # Calculate bin centers
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

        # Plot as line
        plt.plot(bin_centers, counts, label=model, color=colors[i],
                 linewidth=2, marker='o', markersize=3)

    plt.xlabel('Log Probability Scores')
    plt.ylabel('Density')
    plt.title('Distribution of Logprob Scores by Model (Histogram as Line)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def simple_hist(logprobs, data, task="Morally Acceptable", idx=1):
    # # Create histogram line plot for each model
    plt.figure(figsize=(12, 8))
    for model in data['model'].unique():
        model_data = data[(data['model'] == model)]
        if model=="deepseek-r1":
            model_data['statement_id'] = np.tile(np.arange(1003), 2)
        else:
            model_data['statement_id'] = np.tile(np.arange(1003), 3)
        mean_model_data = model_data.groupby(['statement_id', 'model'])[logprobs].apply(lambda x: np.exp(x).median())

        mean_model_data = mean_model_data.dropna()

        counts, bin_edges = np.histogram(mean_model_data, bins=50)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        model = model_mapping[model] if model in model_mapping.keys() else model
        plt.plot(bin_centers, counts, label=model, linewidth=2, marker='o', markersize=4)

    plt.ylabel('Statement Answer Counts (averaged over 3 runs)')
    plt.title(f"{task} Token Probability Histogram")
    plt.legend(loc='upper left')
    plt.grid(True, alpha=0.3)
    # plt.xlim(-.05, 0)  # Zoom to x-axis range from -1 to 0
    plt.ylim(0, 1000)
    ax = plt.gca()  # Get current axis
    ax.set_yticklabels([])  # Remove y-axis tick labels
    ax.set_ylabel('')  # Remove y-axis label
    ax.tick_params(left=False)
    plt.xlabel(f"Probability (%) of {task} Token as an Answer to Task {idx}")
    plt.savefig(f"figure_11_{logprobs}.svg",  dpi=300, bbox_inches='tight')
    plt.savefig(f"figure_11_{logprobs}.png",  dpi=300, bbox_inches='tight')
    plt.show()

    plt.close()


def plot_cdf(logprobs, logprobs2, data): #works
    df = data
    import matplotlib.pyplot as plt
    import numpy as np
    X=0.9

    # Create CDF plot with two logprobs datasets
    plt.figure(figsize=(12, 8))

    # Get unique models and create color palette
    models = df['model'].unique()
    colors = plt.cm.Set1(np.linspace(0, 1, len(models)))
    vals1 = {}
    vals2  ={}
    # First dataset (logprobs) - solid lines
    for i, model in enumerate(models):
        model_data = df[df['model'] == model]

        if model=="deepseek-r1":
            model_data['statement_id'] = np.tile(np.arange(1003), 2)
        else:
            model_data['statement_id'] = np.tile(np.arange(1003), 3)
        # mean_model_data = model_data.groupby(['statement_id', 'model'])[logprobs].mean()
        # mean_model_data = mean_model_data[(mean_model_data >=X)]
        mean_model_data = model_data.groupby(['statement_id', 'model'])[logprobs].apply(lambda x: np.exp(x).mean())
        mean_model_data = mean_model_data[mean_model_data >= X]
        vals1.update({model:len(mean_model_data)/1003 *100})

        # Remove NaN values
        mean_model_data = mean_model_data.dropna()
        # Sort the data
        sorted_data = np.sort(mean_model_data)

        # Create y-values (cumulative probability)
        y_values = np.arange(1, len(sorted_data) + 1) / len(sorted_data)

        # Plot CDF with solid line
        plt.plot(sorted_data, y_values, label=f'{model} (MW)', linewidth=2,
                 color=colors[i], linestyle='-')

    # Second dataset (logprobs2) - dashed lines
    for i, model in enumerate(models):
        model_data = df[df['model'] == model]

        if model=="deepseek-r1":
            model_data['statement_id'] = np.tile(np.arange(1003), 2)
        else:
            model_data['statement_id'] = np.tile(np.arange(1003), 3)
        mean_model_data = model_data.groupby(['statement_id', 'model'])[logprobs2].apply(lambda x: np.exp(x).mean())
        mean_model_data = mean_model_data[mean_model_data >= X]
        vals2.update({model:len(mean_model_data)/1003 *100})

        # Remove NaN values
        mean_model_data = mean_model_data.dropna()

        # Skip if no data after removing NaNs
        if len(mean_model_data) == 0:
            continue
        # filtered_data = mean_model_data[(mean_model_data[logprobs] >X)][logprobs]

        # Sort the data
        sorted_data = np.sort(mean_model_data)

        # Create y-values (cumulative probability)
        y_values = np.arange(1, len(sorted_data) + 1) / len(sorted_data)

        # Plot CDF with dashed line
        plt.plot(sorted_data, y_values, label=f'{model} (SP)', linewidth=2,
                 color=colors[i], linestyle='--')
    # Get current x-tick positions (log-probabilities)
    xticks = plt.gca().get_xticks()

    # Transform to probabilities and then to percentages
    percent_labels = np.exp(xticks) * 100
    # Format as percentage strings, rounded to 1 decimal place
    percent_labels_str = [f"{p:.1f}%" for p in percent_labels]
    # Set new x-tick labels
    plt.gca().set_xticklabels(percent_labels_str)
    plt.xlabel("Probability (%) of 'Speciesist' Answer to Task 1 and 'Morally Acceptable' to Task 2")

    # plt.xlabel('Log Probability Scores')
    plt.ylabel('Cumulative Probability')
    plt.title('Cumulative Distribution Function (CDF) by Model - Two Questions')
    plt.legend()
    plt.grid(True, alpha=0.3)
    # plt.xlim(90, 100)  # Focus on your range of interest
    plt.show()

    print(vals1)
    print(vals2)


def plot_bars():
    import matplotlib.pyplot as plt
    import numpy as np

    # Your data
    vals1 = {'gpt-3.5': 55.732801595214355, 'gpt-4o': 55.1345962113659, 'gpt-4.1': 67.59720837487538,
             'llama-3.1-405b': 58.225324027916244, 'llama3.3-70b': 43.868394815553344,
             'llama-4-maverick': 56.33100697906281, 'grok-3': 57.82652043868395,
             'deepseek-v3': 60.219341974077764, 'deepseek-r1': 60.11964107676969}

    vals2 = {'gpt-3.5': 62.412761714855435, 'gpt-4o': 96.7098703888335, 'gpt-4.1': 98.60418743768695,
             'llama-3.1-405b': 84.64606181455633, 'llama3.3-70b': 95.91226321036889,
             'llama-4-maverick': 87.53738783649054, 'grok-3': 86.14157527417746,
             'deepseek-v3': 80.6580259222333, 'deepseek-r1': 73.57926221335993}

    models = list(vals1.keys())
    x = np.arange(len(models))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots(figsize=(12, 6))
    rects1 = ax.bar(x - width / 2, [vals1[m] for m in models], width, label='Dataset 1')
    rects2 = ax.bar(x + width / 2, [vals2[m] for m in models], width, label='Dataset 2')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Percentage (%)')
    ax.set_title('Percentage Above Threshold by Model')
    ax.set_xticks(x)
    ax.set_xticklabels(models, rotation=30, ha='right')
    ax.legend()

    # Optionally, add value labels on top of bars
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.1f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8)

    autolabel(rects1)
    autolabel(rects2)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    data = pd.read_csv("logprobs.csv", index_col=[0])
    cols = [ 'acceptable_logs', 'wrong_logs', 'speciesist_logs', 'nospeciesist_logs']
    data[cols] = data[cols].replace("NONE",np.nan)
    data[cols] = data[cols].astype(float)

    logprobs = "acceptable_logs"
    logprobs2 = "speciesist_logs"
    simple_hist(logprobs, data, task="Morally Acceptable", idx=1)
    simple_hist(logprobs2, data, task="Speciesist", idx=2)

    plot_cdf(logprobs, logprobs2, data)
