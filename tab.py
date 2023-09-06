import os
import json
import platform

# Function to clear the terminal screen based on the operating system
def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def create_blank_tab(num_measures, num_ticks, num_strings):
    tab = {
        "measures": [num_ticks] * num_measures,
        "strings": [[["-"] * num_ticks for _ in range(num_strings)] for _ in range(num_measures)],
    }
    return tab

def display_measure(tab, measure):
    num_measures = len(tab["measures"])
    print(f"Measure {measure + 1} / {num_measures}:")
    for string_num, notes in enumerate(tab["strings"][measure]):
        notes_str = "".join(notes)
        print(f"{string_num + 1}|{notes_str}|")
    print()

def export_tab_to_text_file(tab, title, filename):
    with open(filename, "w") as file:
        file.write(f"{title}\n\n")
        for measure_num, measure in enumerate(tab["strings"]):
            file.write(f"Measure {measure_num + 1} / {len(tab['measures'])}:\n")
            for string_num, notes in enumerate(measure):
                notes_str = "".join(notes)
                file.write(f"{string_num + 1}|{notes_str}|\n")
            file.write("\n")

    print(f"Tab exported to {filename} with the title: {title}")

def edit_tab(tab):
    current_measure = 0
    num_measures = len(tab["measures"])
    while True:
        clear_screen()
        display_measure(tab, current_measure)
        print(f"\nCurrent Measure: {current_measure + 1} / {num_measures}\n")
        print("Options:")
        print("1. Edit a note")
        print("2. Next measure")
        print("3. Previous measure")
        print("4. Save tab to JSON file")
        print("5. Load tab from JSON file")
        print("6. Export tab to text file")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            measure = current_measure
            string_num = int(input("Enter the string number (1-6) to edit: ")) - 1
            position = int(input(f"Enter the position in the measure (1-{tab['measures'][measure]}) for string {string_num + 1}: ")) - 1
            note = input("Enter the note: ")
            if 0 <= string_num < num_strings and 0 <= position < tab["measures"][measure]:
                tab["strings"][measure][string_num][position] = note
        elif choice == "2":
            if current_measure < num_measures - 1:
                current_measure += 1
        elif choice == "3":
            if current_measure > 0:
                current_measure -= 1
        elif choice == "4":
            filename = input("Enter the filename to save to: ")
            with open(filename, "w") as file:
                json.dump(tab, file, indent=4)
            print(f"Tab saved to {filename}")
        elif choice == "5":
            filename = input("Enter the filename to load from: ")
            try:
                with open(filename, "r") as file:
                    tab = json.load(file)
                num_measures = len(tab["measures"])
                print(f"Tab loaded from {filename}")
            except FileNotFoundError:
                print(f"File {filename} not found.")
        elif choice == "6":
            title = input("Enter the title for the tab: ")
            filename = input("Enter the filename to export to: ")
            export_tab_to_text_file(tab, title, filename)
        elif choice == "7":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    num_measures = int(input("Enter the number of measures in your tab: "))
    num_ticks = int(input("Enter the number of ticks in each measure: "))
    num_strings = int(input("Enter the number of strings on your instrument: "))

    tab = create_blank_tab(num_measures, num_ticks, num_strings)

    edit_tab(tab)
