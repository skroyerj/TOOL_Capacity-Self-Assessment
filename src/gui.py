import matplotlib.pyplot as plt
import likert_conversion
import visualisation

def show_visualization_menu(dataframes, likert_questions, REV_LIKERTS):
    while True:
        print("\n" + "="*50)
        print("LIKERT SCALE VISUALIZATION MENU")
        print("="*50)
        print("1. Question over time")
        print("2. Distribution for specific week")
        print("3. Heatmap for specific week")
        print("4. Summary report (all questions)")
        print("5. Histogram for specific weeks")
        print("6. Exit")

        choice = input("\nEnter choice (1-6): ")

        if choice == '1':
            print("\nAvailable Questions:")
            for i, question in enumerate(likert_questions, start=1):
                print(f"{i}. {question}")
            
            question = input(f"\nEnter choice (1-{len(likert_questions)}): ")

            question = likert_questions[int(question)-1]

            fig = visualisation.plot_question_over_time(dataframes, question)
            plt.show()
        elif choice == '2':
            print("\nAvailable Questions:")
            for i, question in enumerate(likert_questions, start=1):
                print(f"{i}. {question}")
            
            question = input(f"\nEnter choice (1-{len(likert_questions)}): ")

            mapping = []

            if int(question) <= 12:
                mapping = REV_LIKERTS["likert_6pt"]

            elif int(question) == 13 or int(question) == 14:
                mapping = REV_LIKERTS["likert_7pt_1"]
            
            elif int(question) == 15:
                mapping = REV_LIKERTS["likert_7pt_2"]

            print("Likert mapping selected:", mapping)

            question = likert_questions[int(question)-1]

            raw_input = input("Enter week number (comma separated, 5-9, or 0 for all weeks): ")

            weeks = [
                int(w.strip())
                for w in raw_input.split(',')
                if w.strip().isdigit()
            ]


            if weeks == [0]:
                weeks = None  # Brug None for at indikere alle uger

            fig = visualisation.plot_stacked_distribution_multiweek(dataframes, question, weeks, likert_mapping=mapping, title=None)
            plt.show()
        elif choice == '3':
            print("\nAvailable Questions:")
            for i, question in enumerate(likert_questions, start=1):
                print(f"{i}. {question}")
            raw_input = input(f"\nEnter choices (comma separated, 1-{len(likert_questions)}): ")
            # Konverter input til liste af indeks
            selected_indices = [
                int(i.strip()) - 1
                for i in raw_input.split(',')
                if i.strip().isdigit()
                and 1 <= int(i.strip()) <= len(likert_questions)
            ]

            if not selected_indices:
                print("No valid questions selected.")
                return

            selected_questions = [likert_questions[i] for i in selected_indices]

            raw_input = input("Enter week number (comma separated, 5-9, or 0 for all weeks): ")

            weeks = [
                int(w.strip())
                for w in raw_input.split(',')
                if w.strip().isdigit()
            ]

            if weeks == [0]:
                weeks = None  # Brug None for at indikere alle uger

            fig = visualisation.plot_heatmap_questions_grid(dataframes, selected_questions, weeks)
            plt.show()

        elif choice == '4':
            print("\nAvailable Questions:")
            for i, question in enumerate(likert_questions, start=1):
                print(f"{i}. {question}")
            raw_input = input(f"\nEnter choices (comma separated, 1-{len(likert_questions)}): ")

            # Konverter input til liste af indeks
            selected_indices = [
                int(i.strip()) - 1
                for i in raw_input.split(',')
                if i.strip().isdigit()
                and 1 <= int(i.strip()) <= len(likert_questions)
            ]

            if not selected_indices:
                print("No valid questions selected.")
                return

            selected_questions = [likert_questions[i] for i in selected_indices]

            fig = visualisation.create_summary_report(dataframes, selected_questions)
            plt.show()

        elif choice == '5':
            print("\nAvailable Questions:")
            for i, question in enumerate(likert_questions, start=1):
                print(f"{i}. {question}")
            
            raw_input = input(f"\nEnter choices (comma separated, 1-{len(likert_questions)}): ")

            # Konverter input til liste af indeks
            selected_indices = [
                int(i.strip()) - 1
                for i in raw_input.split(',')
                if i.strip().isdigit()
                and 1 <= int(i.strip()) <= len(likert_questions)
            ]

            if not selected_indices:
                print("No valid questions selected.")
                return

            selected_questions = [likert_questions[i] for i in selected_indices]

            raw_input = input("Enter week number (comma separated, 5-9, or 0 for all weeks): ")

            weeks = [
                int(w.strip())
                for w in raw_input.split(',')
                if w.strip().isdigit()
            ]

            fig = visualisation.plot_histogram_multiweek(dataframes,selected_questions, weeks, bins=10, title=None)
            plt.show()


        elif choice == '6':
            break
        else:
            print("Invalid choice!")