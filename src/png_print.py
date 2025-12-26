import matplotlib.pyplot as plt

import visualisation
from main_analysis import LIKERTS
from main_analysis import dataframes

import os
# print(os.getcwd())

"""
PRINTING PNGS
"""
dir_path = "figures/"
os.makedirs(dir_path, exist_ok=True)

# Weeks 5,7,9 stacked bar chart for Q10 to Q12

weeks = [5, 7, 9]
likert_questions = [
    "The teacher",
    "The TA's",
    "Other students"
]

for i, q in enumerate(likert_questions, start=10):
    fig = visualisation.plot_stacked_distribution_multiweek(
        dataframes,
        q,
        weeks,
        LIKERTS["likert_6pt"]
    )

    fig.savefig(
        f"{dir_path}stacked_W5-7-9_Q{i}.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.close(fig)


# Weeks 5,7,9 heatmaps for Q10, Q11, Q12

fig = visualisation.plot_heatmap_questions_grid(
    dataframes,
    likert_questions,
    weeks
    )

fig.savefig(
    f"{dir_path}heatmap_W5-7-9_Q10-11-12.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close(fig)


# -------------------------------------------------------------------------------
# Summary for Q10, Q11, Q12 across all weeks
"""
fig = visualisation.create_summary_report(
    dataframes,
    likert_questions
    )

fig.savefig(
    f"{dir_path}summary_Q10-11-12.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close(fig)
"""

# ------------------------------------------------------------------------------
# Individual mappings for Q1-9
# """
likert_questions = ["I felt confident in working with the methodology today",
    "I am interested in the methodology of this course",
    "This course is relevant for me in my future",
    "I want to gain practical knowledge",
    "I want to gain theoretical knowledge",
    "I feel like I know more than I did last week",
    "I feel that I have influence and responsibility in my group, and that my inclusion and opinions are valued",
    "I feel like I can use my (priorly learned) skills in the course",
    "I feel like I am acquiring new skills every week with the Agile methodology"
    ]

for i, q in enumerate(likert_questions, start=1):
    fig = visualisation.plot_question_over_time(
        dataframes,
        q
    )

    fig.savefig(
        f"{dir_path}over-time_Q{i}.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.close(fig)
# """
# -------------------------------------------------------------------------------
# Stacked distributions for Q1-9
# """
for i, q in enumerate(likert_questions, start=1):
    fig = visualisation.plot_stacked_distribution_multiweek(
        dataframes,
        q,
        weeks,
        LIKERTS["likert_6pt"]
    )

    fig.savefig(
        f"{dir_path}stacked_W5-7-9_Q{i}.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.close(fig)
# """


# ------------------------------------------------------------------------------
# Individual mappings for Q13-15
# """
likert_questions = [
        "How much uncertainty do you encounter in this course regarding the end goal at this point?",
        "How much uncertainty did you encounter in the Agile methodology from today?",
        "How easy or difficult would it be to make changes to your design at this stage?"
    ]

for i, q in enumerate(likert_questions, start=13):
    fig = visualisation.plot_question_over_time(
        dataframes,
        q
    )

    fig.savefig(
        f"{dir_path}over-time_Q{i}.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.close(fig)
# """
# -------------------------------------------------------------------------------
# Stacked distributions for Q13-14
# """
for i, q in enumerate(likert_questions[:2], start=13):
    fig = visualisation.plot_stacked_distribution_multiweek(
        dataframes,
        q,
        weeks,
        LIKERTS["likert_7pt_1"]
    )

    fig.savefig(
        f"{dir_path}stacked_W5-7-9_Q{i}.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.close(fig)

for i, q in enumerate(likert_questions[2:], start=15):
    fig = visualisation.plot_stacked_distribution_multiweek(
        dataframes,
        q,
        weeks,
        LIKERTS["likert_7pt_2"]
    )

    fig.savefig(
        f"{dir_path}stacked_W5-7-9_Q{i}.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.close(fig)
# """