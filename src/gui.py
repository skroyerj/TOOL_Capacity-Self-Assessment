import matplotlib.pyplot as plt
import visualisation

def show_visualization_menu(dataframes, likert_questions):
    while True:
        print("\n" + "="*50)
        print("LIKERT SCALE VISUALIZATION MENU")
        print("="*50)
        print("1. Question over time")
        print("2. Distribution for specific week")
        print("3. Heatmap for specific week")
        print("4. Summary report (all questions)")
        print("5. Exit")
        
        choice = input("\nEnter choice (1-5): ")
        
        if choice == '1':
            print("\nAvailable Questions:")
            for i, question in enumerate(likert_questions, start=1):
                print(f"{i}. {question}")
            
            question = input(f"\nEnter choice (1-{len(likert_questions)}): ")
            question = likert_questions[int(question)-1]
            fig = visualisation.plot_question_over_time(dataframes, question)
            plt.show()
        elif choice == '2':
            question = input("Enter question column name: ")
            week = int(input("Enter week number: "))
            fig = visualisation.plot_stacked_distribution(dataframes, question, week)
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

            week = int(input("Enter week number: "))

            if week == 0:
                week = None  # Brug None for at indikere alle uger

            fig = visualisation.plot_heatmap_questions_grid(dataframes, selected_questions, week)
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
            break
        else:
            print("Invalid choice!")