import matplotlib.pyplot as plt
import numpy as np


def visualise(categories,
    main_cat1_name, main_cat2_name,
    subcat1_name, subcat2_name,
    main_cat1_subcat1_data, main_cat1_subcat2_data,
    main_cat2_subcat1_data, main_cat2_subcat2_data,
    colors=None,
    title='Speciesism benchmark',
    xlabel='Models',
    ylabel='Answers (percentage)',
    figsize=(12, 7)):

    # Default colors if not provided
    if colors is None:
        colors = {
            main_cat1_name: 'red',
            main_cat2_name: 'lightgreen',
            subcat1_name: 'orange',
            subcat2_name: 'darkgreen'
        }

    # Default labels if not provided
    if title is None:
        title = f'Distribution by {main_cat1_name}/{main_cat2_name} and {subcat1_name}/{subcat2_name}'
    if xlabel is None:
        xlabel = 'Categories'
    if ylabel is None:
        ylabel = 'Count'

    # Set the width of the bars
    bar_width = 0.35

    # Set positions for the bars
    x = np.arange(len(categories))

    # Create the figure and axis
    fig, ax = plt.subplots(figsize=figsize)

    # Create the stacked bars
    bar1_bottom = ax.bar(x - bar_width / 2, main_cat1_subcat1_data, bar_width,
                         label=f'{main_cat1_name}',
                         color=colors[main_cat1_name])

    bar1_top = ax.bar(x - bar_width / 2, main_cat1_subcat2_data, bar_width,
                      bottom=main_cat1_subcat1_data,
                      label=f'{main_cat2_name}',
                      color=colors[main_cat2_name])

    bar2_bottom = ax.bar(x + bar_width / 2, main_cat2_subcat1_data, bar_width,
                         label=f'{subcat1_name}',
                         color=colors[subcat1_name])

    bar2_top = ax.bar(x + bar_width / 2, main_cat2_subcat2_data, bar_width,
                      bottom=main_cat2_subcat1_data,
                      label=f'{subcat2_name}',
                      color=colors[subcat2_name])

    # Add labels, title and legend
    ax.set_xlabel(xlabel, fontweight='bold')
    ax.set_ylabel(ylabel, fontweight='bold')
    ax.set_title(title, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))

    # Helper function to add value labels on each segment
    def add_labels(bars, labels):
        for bar, label in zip(bars, labels):
            height = bar.get_height()
            if height > 0:  # Only show labels for non-zero values
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_y() + height / 2,
                    str(label),
                    ha='center',
                    va='center',
                    color='black',
                    fontweight='bold')

    # Add the counts to each segment
    add_labels(bar1_bottom, main_cat1_subcat1_data)
    add_labels(bar1_top, main_cat1_subcat2_data)
    add_labels(bar2_bottom, main_cat2_subcat1_data)
    add_labels(bar2_top, main_cat2_subcat2_data)

    # Add a light grid for better readability
    ax.yaxis.grid(True, linestyle='--', alpha=0.7)

    # Adjust layout to make room for the legend
    plt.tight_layout(rect=[0, 0, 0.85, 1])
    plt.show()
    return fig, ax


def plot(data):
    models =[]
    group1_type1 = []
    group1_type2 = []
    group2_type1 = []
    group2_type2 = []
    for val in data:
        models.append(val["model"])
        group1_type1.append(val["wrong"])
        group1_type2.append(val["not wrong"])
        group2_type1.append(val["speciesist"])
        group2_type2.append(val["not speciesist"])

    # Create and display the chart
    fig, ax = visualise(
        categories=models,
        main_cat1_subcat1_data=group1_type1,
        main_cat1_subcat2_data=group1_type2,
        main_cat2_subcat1_data=group2_type1,
        main_cat2_subcat2_data=group2_type2,
        main_cat1_name='wrong',
        main_cat2_name='not wrong',
        subcat1_name='speciesist',
        subcat2_name='not speciesist',
        title='SpeciesismBench',
        xlabel='Models',
        ylabel='Answers (percentage)',
        figsize=(14, 8)
    )

    plt.show()

# Example usage:
if __name__ == "__main__":
    data = [
        {'not wrong': 583, 'wrong': 360, 'speciesist': 778, 'not speciesist': 178, 'model': 'gpt-3.5'},
        {'not wrong': 598, 'wrong': 389, 'speciesist': 718, 'not speciesist': 283, 'model': 'gpt-3.5'},
        {'not wrong': 596, 'wrong': 388, 'speciesist': 708, 'not speciesist': 291, 'model': 'gpt-3.5'},
        {'not wrong': 578, 'wrong': 404, 'speciesist': 992, 'not speciesist': 11, 'model': 'gpt-4o'},
        {'not wrong': 660, 'wrong': 341, 'speciesist': 984, 'not speciesist': 19, 'model': 'gpt-4o'},
        {'not wrong': 665, 'wrong': 337, 'speciesist': 984, 'not speciesist': 19, 'model': 'gpt-4o'},
        {'not wrong': 694, 'wrong': 309, 'speciesist': 991, 'not speciesist': 12, 'model': 'gpt-4.1'},
        {'not wrong': 700, 'wrong': 303, 'speciesist': 990, 'not speciesist': 13, 'model': 'gpt-4.1'},
        {'not wrong': 702, 'wrong': 301, 'speciesist': 990, 'not speciesist': 13, 'model': 'gpt-4.1'},
        {'not wrong': 0, 'wrong': 311, 'speciesist': 0, 'not speciesist': 0, 'model': 'o1'},
        {'not wrong': 629, 'wrong': 374, 'speciesist': 985, 'not speciesist': 18, 'model': 'o1'},
        {'not wrong': 631, 'wrong': 372, 'speciesist': 977, 'not speciesist': 26, 'model': 'o1'},
        {'not wrong': 0, 'wrong': 205, 'speciesist': 0, 'not speciesist': 0, 'model': 'o3-mini'},
        {'not wrong': 765, 'wrong': 238, 'speciesist': 464, 'not speciesist': 539, 'model': 'o3-mini'},
        {'not wrong': 762, 'wrong': 241, 'speciesist': 458, 'not speciesist': 545, 'model': 'o3-mini'},
        {'not wrong': 456, 'wrong': 336, 'speciesist': 703, 'not speciesist': 89, 'model': 'gemini-1.5'},
        {'not wrong': 524, 'wrong': 479, 'speciesist': 889, 'not speciesist': 114, 'model': 'gemini-1.5'},
        {'not wrong': 531, 'wrong': 472, 'speciesist': 888, 'not speciesist': 115, 'model': 'gemini-1.5'},
        {'not wrong': 662, 'wrong': 341, 'speciesist': 958, 'not speciesist': 45, 'model': 'gemini-2'},
        {'not wrong': 664, 'wrong': 339, 'speciesist': 955, 'not speciesist': 48, 'model': 'gemini-2'},
        {'not wrong': 664, 'wrong': 339, 'speciesist': 956, 'not speciesist': 47, 'model': 'gemini-2'},
        {'not wrong': 700, 'wrong': 303, 'speciesist': 888, 'not speciesist': 115, 'model': 'gemini-2.5'},
        {'not wrong': 699, 'wrong': 304, 'speciesist': 889, 'not speciesist': 114, 'model': 'gemini-2.5'},
        {'not wrong': 698, 'wrong': 305, 'speciesist': 890, 'not speciesist': 113, 'model': 'gemini-2.5'},
        {'not wrong': 704, 'wrong': 299, 'speciesist': 848, 'not speciesist': 155, 'model': 'claude-3.5'},
        {'not wrong': 703, 'wrong': 300, 'speciesist': 847, 'not speciesist': 156, 'model': 'claude-3.5'},
        {'not wrong': 707, 'wrong': 296, 'speciesist': 841, 'not speciesist': 162, 'model': 'claude-3.5'},
        {'not wrong': 810, 'wrong': 193, 'speciesist': 784, 'not speciesist': 219, 'model': 'claude-3.7'},
        {'not wrong': 811, 'wrong': 192, 'speciesist': 779, 'not speciesist': 224, 'model': 'claude-3.7'},
        {'not wrong': 808, 'wrong': 195, 'speciesist': 782, 'not speciesist': 221, 'model': 'claude-3.7'},
        {'not wrong': 789, 'wrong': 214, 'speciesist': 835, 'not speciesist': 168, 'model': 'claude-4'},
        {'not wrong': 788, 'wrong': 215, 'speciesist': 835, 'not speciesist': 168, 'model': 'claude-4'},
        {'not wrong': 788, 'wrong': 214, 'speciesist': 834, 'not speciesist': 168, 'model': 'claude-4'},
        {'not wrong': 684, 'wrong': 318, 'speciesist': 927, 'not speciesist': 76, 'model': 'llama3.1'},
        {'not wrong': 680, 'wrong': 323, 'speciesist': 924, 'not speciesist': 78, 'model': 'llama3.1'},
        {'not wrong': 690, 'wrong': 311, 'speciesist': 921, 'not speciesist': 82, 'model': 'llama3.1'},
        {'not wrong': 474, 'wrong': 529, 'speciesist': 964, 'not speciesist': 39, 'model': 'llama3.3-70b'},
        {'not wrong': 474, 'wrong': 529, 'speciesist': 968, 'not speciesist': 35, 'model': 'llama3.3-70b'},
        {'not wrong': 462, 'wrong': 541, 'speciesist': 967, 'not speciesist': 36, 'model': 'llama3.3-70b'},
        {'not wrong': 575, 'wrong': 428, 'speciesist': 885, 'not speciesist': 118, 'model': 'llama4'},
        {'not wrong': 579, 'wrong': 424, 'speciesist': 900, 'not speciesist': 103, 'model': 'llama4'},
        {'not wrong': 571, 'wrong': 432, 'speciesist': 892, 'not speciesist': 111, 'model': 'llama4'},
        {'not wrong': 612, 'wrong': 391, 'speciesist': 898, 'not speciesist': 104, 'model': 'grok-3'},
        {'not wrong': 620, 'wrong': 383, 'speciesist': 893, 'not speciesist': 110, 'model': 'grok-3'},
        {'not wrong': 610, 'wrong': 393, 'speciesist': 891, 'not speciesist': 112, 'model': 'grok-3'},
        {'not wrong': 675, 'wrong': 328, 'speciesist': 881, 'not speciesist': 122, 'model': 'deepseek-v3'},
        {'not wrong': 675, 'wrong': 328, 'speciesist': 879, 'not speciesist': 124, 'model': 'deepseek-v3'},
        {'not wrong': 675, 'wrong': 328, 'speciesist': 879, 'not speciesist': 124, 'model': 'deepseek-v3'},
        {'not wrong': 607, 'wrong': 396, 'speciesist': 765, 'not speciesist': 238, 'model': 'deepseek-r1'},
        {'not wrong': 599, 'wrong': 404, 'speciesist': 768, 'not speciesist': 235, 'model': 'deepseek-r1'},

    ]
    normalised_data = []
    for d in data:
        new_d = {}
        # den = sum([val for key, val in d.items() if type(val)==int])
        for k,v in d.items():
            if type(v) == int:
                new_d[k] =int( v*100/1003)
            else:
                new_d["model"] = v
        normalised_data.append(new_d)
    print(data)
    print(normalised_data)
    plot(normalised_data)
