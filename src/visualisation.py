import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)

def restructure_flat_dict(flat_dict):
    """
    Convert flat dictionary to nested structure for visualization.
    
    Input format: {'oth_students_Week5': df, 'cs_students_Week5': df, ...}
    Output format: {5: {'oth_students': df, 'cs_students': df}, 6: {...}, ...}
    """
    nested = {}
    
    for key, df in flat_dict.items():
        # Split by '_Week' to get education and week
        parts = key.split('_Week')
        if len(parts) == 2:
            education = parts[0]
            week = int(parts[1])
            
            if week not in nested:
                nested[week] = {}
            
            nested[week][education] = df
    
    return nested

# def prepare_likert_data(dataframes_dict, likert_columns):
    """
    Prepare data from multiple weeks and education groups.
    
    Parameters:
    - dataframes_dict: dict with structure {week: {education: df}}
      e.g., {1: {'CS': df1, 'DS': df2}, 2: {...}, ...}
    - likert_columns: list of column names that contain Likert scale questions
    
    Returns:
    - prepared_data: dict with aggregated statistics
    """
    prepared = {}
    
    for week, edu_dfs in dataframes_dict.items():
        prepared[week] = {}
        for education, df in edu_dfs.items():
            prepared[week][education] = {}
            for col in likert_columns:
                if col in df.columns:
                    # Calculate mean and distribution
                    prepared[week][education][col] = {
                        'mean': df[col].mean(),
                        'std': df[col].std(),
                        'counts': df[col].value_counts().to_dict(),
                        'n': df[col].notna().sum()
                    }
    
    return prepared

def plot_question_over_time(dataframes_dict, question_col, title=None):
    """
    Plot a single question's responses over time, grouped by education.
    Shows median with interquartile range (IQR).
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    weeks = sorted(dataframes_dict.keys())
    education_programs = set()
    for week_data in dataframes_dict.values():
        education_programs.update(week_data.keys())
    
    colors = sns.color_palette("husl", len(education_programs))
    
    for edu, color in zip(sorted(education_programs), colors):
        medians = []
        q1s = []
        q3s = []
        ns = []
        
        for week in weeks:
            if edu in dataframes_dict[week] and question_col in dataframes_dict[week][edu].columns:
                df = dataframes_dict[week][edu]
                values = df[question_col].dropna()
                
                if len(values) > 0:
                    medians.append(values.median())
                    q1s.append(values.quantile(0.25))
                    q3s.append(values.quantile(0.75))
                    ns.append(len(values))
                else:
                    medians.append(np.nan)
                    q1s.append(np.nan)
                    q3s.append(np.nan)
                    ns.append(0)
            else:
                medians.append(np.nan)
                q1s.append(np.nan)
                q3s.append(np.nan)
                ns.append(0)
        
        # Plot median line
        ax.plot(
            weeks, medians,
            marker='o', label=edu,
            color=color, linewidth=2, markersize=8
        )
        
        # Plot IQR band (Q1–Q3)
        ax.fill_between(
            weeks, q1s, q3s,
            alpha=0.25, color=color
        )
    
    ax.set_xlabel('Week', fontsize=12)
    ax.set_ylabel('Median Score', fontsize=12)
    ax.set_title(title or question_col, fontsize=14, fontweight='bold')
    ax.legend(title='Education', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.set_xticks(weeks)
    ax.set_ylim(1, 6)
    ax.set_yticks(range(1, 7))
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


def plot_stacked_distribution(dataframes_dict, question_col, week, title=None):
    """
    Plot stacked bar chart showing distribution of responses for one question
    across education programs for a specific week.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if week not in dataframes_dict:
        print(f"Week {week} not found in data")
        return None
    
    edu_programs = sorted(dataframes_dict[week].keys())
    
    # Get all possible Likert values
    all_values = set()
    for edu in edu_programs:
        if question_col in dataframes_dict[week][edu].columns:
            all_values.update(dataframes_dict[week][edu][question_col].dropna().unique())
    
    likert_values = sorted(all_values)
    
    # Prepare data
    data = {val: [] for val in likert_values}
    
    for edu in edu_programs:
        if question_col in dataframes_dict[week][edu].columns:
            counts = dataframes_dict[week][edu][question_col].value_counts()
            total = counts.sum()
            for val in likert_values:
                percentage = (counts.get(val, 0) / total * 100) if total > 0 else 0
                data[val].append(percentage)
        else:
            for val in likert_values:
                data[val].append(0)
    
    # Create stacked bars
    bottom = np.zeros(len(edu_programs))
    colors = sns.color_palette("vlag_r", len(likert_values))
    
    for val, color in zip(likert_values, colors):
        ax.bar(edu_programs, data[val], bottom=bottom, label=f'{val}', color=color)
        bottom += data[val]
    
    ax.set_ylabel('Percentage', fontsize=12)
    ax.set_title(title or f'{question_col} - Week {week}', fontsize=14, fontweight='bold')
    ax.legend(title='Response', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.set_ylim(0, 100)
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig

def plot_stacked_distribution_multiweek(
    dataframes_dict,
    question_col,
    weeks,
    title=None
):
    # Tillad både int og liste
    if isinstance(weeks, int):
        weeks = [weeks]

    weeks = [w for w in weeks if w in dataframes_dict]
    if not weeks:
        print("No valid weeks provided")
        return None

    # Find alle education programs på tværs af uger
    edu_programs = sorted({
        edu
        for w in weeks
        for edu in dataframes_dict[w].keys()
    })

    likert_values = [1,2,3,4,5,6]  # Antag faste Likert-værdier

    n_weeks = len(weeks)
    n_cols = n_weeks if n_weeks <= 3 else 3
    n_rows = (n_weeks + n_cols - 1) // n_cols

    fig, axes = plt.subplots(
        n_rows, n_cols,
        figsize=(18, 5 * n_rows),
        squeeze=False
    )

    colors = sns.color_palette("vlag_r", len(likert_values))

    for idx, week in enumerate(weeks):
        ax = axes[idx // n_cols][idx % n_cols]

        data = {val: [] for val in likert_values}

        for edu in edu_programs:
            if (
                edu in dataframes_dict[week]
                and question_col in dataframes_dict[week][edu].columns
            ):
                counts = dataframes_dict[week][edu][question_col].value_counts()
                total = counts.sum()
                for val in likert_values:
                    pct = (counts.get(val, 0) / total * 100) if total > 0 else 0
                    data[val].append(pct)
            else:
                for val in likert_values:
                    data[val].append(0)

        bottom = np.zeros(len(edu_programs))
        for val, color in zip(likert_values, colors):
            ax.bar(
                edu_programs,
                data[val],
                bottom=bottom,
                label=str(val),
                color=color
            )
            bottom += data[val]

        ax.set_title(f"Week {week}", fontsize=12, fontweight="bold")
        ax.set_ylim(0, 100)
        ax.tick_params(axis="x", rotation=45)

        # Kun venstre kolonne får y-label
        if idx % n_cols == 0:
            ax.set_ylabel("Percentage", fontsize=12)
        else:
            ax.tick_params(axis="y", labelleft=False)
        
        

    # Skjul tomme subplots
    for idx in range(n_weeks, n_rows * n_cols):
        axes[idx // n_cols][idx % n_cols].set_visible(False)

    # # Fælles legend
    # handles, labels = ax.get_legend_handles_labels()
    # ax.legend(
    #     handles,
    #     labels,
    #     title="Response",
    #     bbox_to_anchor=(1.02, 0.5),
    #     loc="center left"
    # )
    ax.legend(title='Response', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.set_ylim(0, 100)

    plt.suptitle(
        title or f"{question_col}",
        fontsize=16,
        fontweight="bold",
        y=0.98
    )

    # plt.tight_layout()
    fig.subplots_adjust(
    left=0.05,
    right=0.9,
    top=0.85,
    bottom=0.175,
    wspace=0.3,
    hspace=0.4
)
    return fig

def plot_heatmap_questions_grid(dataframes_dict,
    likert_columns,
    weeks=None):

    if weeks is None:
        weeks = sorted(dataframes_dict.keys())

    # collect all education programs across all weeks
    education_programs = sorted({
        edu
        for week_data in dataframes_dict.values()
        for edu in week_data.keys()
    })

    n_weeks = len(weeks)
    n_cols = n_weeks if n_weeks <= 3 else 3
    n_rows = (n_weeks + n_cols - 1) // n_cols

    fig, axes = plt.subplots(
        n_rows, n_cols,
        figsize=(18, 5 * n_rows),
        squeeze=False
    )

    # Create axis for shared colorbar (right side)
    cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])

    for idx, week in enumerate(weeks):
        ax = axes[idx // n_cols][idx % n_cols]

        matrix = []
        for question in likert_columns:
            row = []
            for edu in education_programs:
                if (
                    week in dataframes_dict
                    and edu in dataframes_dict[week]
                    and question in dataframes_dict[week][edu].columns
                ):
                    row.append(
                        dataframes_dict[week][edu][question].median()
                    )
                else:
                    row.append(np.nan)
            matrix.append(row)

        short_labels = [
            q[:50] + "..." if len(q) > 50 else q
            for q in likert_columns
        ]

        sns.heatmap(
            matrix,
            xticklabels=education_programs,
            yticklabels=short_labels,
            annot=True,
            fmt=".2f",
            cmap="vlag_r",
            center=3.5,
            vmin=1,
            vmax=6,
            cbar=idx == 0,  # one shared colorbar
            cbar_ax=cbar_ax if idx == 0 else None,
            ax=ax
        )

        ax.set_title(f"Week {week}", fontsize=12, fontweight="bold")
        ax.tick_params(axis="x", rotation=45)

        # Hide y-axis labels for non-left columns
        if idx % n_cols != 0:
            ax.tick_params(axis="y", labelleft=False)

    # Hide unused subplots
    for idx in range(n_weeks, n_rows * n_cols):
        axes[idx // n_cols][idx % n_cols].set_visible(False)

    plt.suptitle(
        "To perform the tasks today, I felt like seeking support from... (median value across all weeks)",
        fontsize=16,
        fontweight="bold",
        y=0.98
    )
    fig.subplots_adjust(
    left=0.07,
    right=0.9,   # plads til colorbar
    top=0.8,
    bottom=0.265,
    wspace=0.13,
    hspace=0.35
    )
    return fig



def create_summary_report(dataframes_dict, likert_columns):
    """
    Create a comprehensive visualization with multiple subplots.
    """
    n_questions = len(likert_columns)
    n_cols = 3
    n_rows = (n_questions + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(16, 5 * n_rows))
    axes = axes.flatten()

    global_min = np.inf
    global_max = -np.inf

    for week_data in dataframes_dict.values():
        for df in week_data.values():
            for col in likert_columns:
                if col in df.columns:
                    global_min = min(global_min, df[col].min())
                    global_max = max(global_max, df[col].max())
    
    weeks = sorted(dataframes_dict.keys())
    education_programs = set()
    for week_data in dataframes_dict.values():
        education_programs.update(week_data.keys())
    
    colors = sns.color_palette("husl", len(education_programs))
    
    for idx, question_col in enumerate(likert_columns):
        ax = axes[idx]
        
        for edu, color in zip(sorted(education_programs), colors):
            means = []
            
            for week in weeks:
                if edu in dataframes_dict[week] and question_col in dataframes_dict[week][edu].columns:
                    df = dataframes_dict[week][edu]
                    means.append(df[question_col].mean())
                else:
                    means.append(np.nan)
            
            ax.plot(weeks, means, marker='o', label=edu, color=color, linewidth=2)
        
        # Shorten title
        short_title = question_col[:60] + '...' if len(question_col) > 60 else question_col
        ax.set_title(short_title, fontsize=10, fontweight='bold')
        ax.set_xlabel('Week', fontsize=9)
        ax.set_ylabel('Mean Score', fontsize=9)
        ax.set_xticks(weeks)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(global_min, global_max)
        
        if idx == 0:
            ax.legend(title='Education', fontsize=8)
        
        col_idx = idx % n_cols

        if col_idx != 0:
            ax.set_ylabel("")
            ax.tick_params(axis="y", labelleft=False)
    
    # Hide extra subplots
    for idx in range(len(likert_columns), len(axes)):
        axes[idx].set_visible(False)
    
    plt.suptitle('Survey Results Over Time - All Questions', 
                 fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout()
    return fig

# Example usage:
"""
# Your flat dictionary structure:
flat_data = {
    'oth_students_Week5': df1,
    'oth_students_Week6': df2,
    'cs_students_Week5': df3,
    'cs_students_Week6': df4,
    # ... etc
}

# Convert to nested structure
dataframes = restructure_flat_dict(flat_data)

# Now dataframes looks like:
# {
#     5: {'oth_students': df1, 'cs_students': df3},
#     6: {'oth_students': df2, 'cs_students': df4},
#     ...
# }

likert_questions = [
    'How confident do you feel?',
    'Rate your understanding',
    # ... other Likert scale questions
]

# Create visualizations:
# 1. Single question over time
fig1 = plot_question_over_time(dataframes, 'How confident do you feel?')
plt.show()

# 2. Distribution for one week
fig2 = plot_stacked_distribution(dataframes, 'How confident do you feel?', week=5)
plt.show()

# 3. Heatmap of all questions for one week
fig3 = plot_heatmap_all_questions(dataframes, likert_questions, week=8)
plt.show()

# 4. Summary of all questions over time
fig4 = create_summary_report(dataframes, likert_questions)
plt.show()
"""