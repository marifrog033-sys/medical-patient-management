import csv
import json
import os
from datetime import date

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")


full_name = input(
    "Enter the full name of the patient separated by space "
    "(Ivanov Ivan Ivanovich): "
)

nameready = "_".join(full_name.split()).title()
patient_path = os.path.join(DATA_DIR, "patients", nameready)

if not os.path.exists(patient_path):
    print("There is no such patient!")
else:
    card_path = os.path.join(patient_path, "card.json")

    if os.path.exists(card_path):
        with open(card_path, "r", encoding="utf-8") as file:
            card = json.load(file)
        print(json.dumps(card, indent=4))
    else:
        print("There is no patient card!")

        surname = input("Enter the surname of the patient: ").capitalize()
        name = input("Enter the name of the patient: ").capitalize()
        patronymic = input(
            "Enter the patronymic of the patient: "
        ).capitalize()
        birth_date = input(
            "Enter the date of birth of the patient (1994-01-10): "
        )
        sex = input("Enter the sex of the patient (M or W): ").upper()

        card = {
            "Surname": surname,
            "Name": name,
            "Patronymic": patronymic,
            "Date of birth": birth_date,
            "Sex": sex,
        }

        with open(card_path, "w", encoding="utf-8") as file:
            json.dump(card, file, indent=4)

        print(json.dumps(card, indent=4))

    separator = "-" * 50
    visits_path = os.path.join(patient_path, "visits")

    while True:
        choice = input(
            f"{separator}\n"
            "Enter:\n"
            " - 1, if you want to see the list of dates of previous visits;\n"
            " - 2, if you want to see the recording of the previous visit;\n"
            " - 3, if you want to start recording in the current visit;\n"
            " - 4, if you want to finish the appointment and complete the program.\n"
            f"{separator}\n"
        )

        if choice == "1":
            if os.path.exists(visits_path):
                print("Previous doctor appointments:")
                for filename in os.listdir(visits_path):
                    print(filename.replace(".txt", ""))
            else:
                print("This is the first appointment with the doctor!")

        elif choice == "2":
            if os.path.exists(visits_path):
                visit_date = input(
                    "Enter the date of the appointment you want to watch: "
                )
                file_path = os.path.join(
                    visits_path, f"{visit_date}.txt"
                )

                if os.path.exists(file_path):
                    with open(file_path, "r", encoding="utf-8") as file:
                        print(file.read())
                else:
                    print("There was no such appointment with the doctor!")
            else:
                print("This is the first appointment with the doctor!")

        elif choice == "3":
            print(
                "Enter records for the current appointment "
                "(to finish press Enter twice): "
            )

            lines = []
            empty_count = 0

            while empty_count < 2:
                line = input()

                if line == "":
                    empty_count += 1
                else:
                    empty_count = 0

                lines.append(line)

            lines = lines[:-2]

            while lines and lines[-1] == "":
                lines.pop()

            os.makedirs(visits_path, exist_ok=True)

            today = date.today()
            visit_file_path = os.path.join(
                visits_path, f"{today}.txt"
            )

            with open(
                visit_file_path, "w", encoding="utf-8"
            ) as file:
                for line in lines:
                    file.write(line + "\n")

                file.write("\n")

        elif choice == "4":
            schedule_path = os.path.join(DATA_DIR, "schedule.csv")

            with open(
                schedule_path,
                "r",
                newline="",
                encoding="utf-8",
            ) as file:
                reader = csv.reader(file)
                rows = list(reader)

            headers = rows[0]
            data = rows[1:]

            csv_name = " ".join(full_name.split()).title()

            for row in data:
                if row[1] == csv_name:
                    row[2] = "Yes"

            with open(
                schedule_path,
                "w",
                newline="",
                encoding="utf-8",
            ) as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                writer.writerows(data)

            break
