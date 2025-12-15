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

def prepare_likert_data(dataframes_dict, likert_columns):
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
    Shows mean with confidence intervals.
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    weeks = sorted(dataframes_dict.keys())
    education_programs = set()
    for week_data in dataframes_dict.values():
        education_programs.update(week_data.keys())
    
    colors = sns.color_palette("husl", len(education_programs))
    
    for edu, color in zip(sorted(education_programs), colors):
        means = []
        stds = []
        ns = []
        
        for week in weeks:
            if edu in dataframes_dict[week] and question_col in dataframes_dict[week][edu].columns:
                df = dataframes_dict[week][edu]
                means.append(df[question_col].mean())
                stds.append(df[question_col].std())
                ns.append(df[question_col].notna().sum())
            else:
                means.append(np.nan)
                stds.append(np.nan)
                ns.append(0)
        
        # Calculate standard error for confidence intervals
        sems = [std / np.sqrt(n) if n > 0 else 0 for std, n in zip(stds, ns)]
        
        ax.plot(weeks, means, marker='o', label=edu, color=color, linewidth=2, markersize=8)
        ax.fill_between(weeks, 
                        [m - 1.96*sem for m, sem in zip(means, sems)],
                        [m + 1.96*sem for m, sem in zip(means, sems)],
                        alpha=0.2, color=color)
    
    ax.set_xlabel('Week', fontsize=12)
    ax.set_ylabel('Mean Score', fontsize=12)
    ax.set_title(title or question_col, fontsize=14, fontweight='bold')
    ax.legend(title='Education', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.set_xticks(weeks)
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

def plot_heatmap_all_questions(dataframes_dict, likert_columns, week):
    """
    Create a heatmap showing mean scores for all questions across education programs
    for a specific week.
    """
    edu_programs = sorted(dataframes_dict[week].keys())
    
    # Build matrix
    matrix = []
    for col in likert_columns:
        row = []
        for edu in edu_programs:
            if col in dataframes_dict[week][edu].columns:
                mean_val = dataframes_dict[week][edu][col].mean()
                row.append(mean_val)
            else:
                row.append(np.nan)
        matrix.append(row)
    
    fig, ax = plt.subplots(figsize=(12, max(8, len(likert_columns) * 0.5)))
    
    # Shorten question labels for readability
    short_labels = [col[:50] + '...' if len(col) > 50 else col for col in likert_columns]
    
    sns.heatmap(matrix, 
                xticklabels=edu_programs,
                yticklabels=short_labels,
                annot=True, 
                fmt='.2f',
                cmap='vlag_r',
                center=3.5,  # Assuming 6-point Likert scale (1-5)
                ax=ax,
                cbar_kws={'label': 'Mean Score'})
    
    ax.set_title(f'Mean Scores by Education Program - Week {week}', 
                 fontsize=14, fontweight='bold', pad=20)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    return fig

def plot_heatmap_questions_grid(dataframes_dict,
    likert_columns,
    weeks=None,
):
    if weeks is None:
        weeks = sorted(dataframes_dict.keys())

    # collect all education programs across all weeks
    education_programs = sorted({
        edu
        for week_data in dataframes_dict.values()
        for edu in week_data.keys()
    })

    n_weeks = len(weeks)
    n_cols = 3
    n_rows = (n_weeks + n_cols - 1) // n_cols

    fig, axes = plt.subplots(
        n_rows, n_cols,
        figsize=(18, 5 * n_rows),
        squeeze=False
    )

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
                        dataframes_dict[week][edu][question].mean()
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
            cbar=idx == 0,  # one shared colorbar
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
        "Mean Likert Scores by Week",
        fontsize=16,
        fontweight="bold",
        y=0.98
    )
    plt.tight_layout()
    return fig



def create_summary_report(dataframes_dict, likert_columns):
    """
    Create a comprehensive visualization with multiple subplots.
    """
    n_questions = len(likert_columns)
    n_cols = 2
    n_rows = (n_questions + 1) // 2
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(16, 5 * n_rows))
    axes = axes.flatten()
    
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
        
        if idx == 0:
            ax.legend(title='Education', fontsize=8)
    
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