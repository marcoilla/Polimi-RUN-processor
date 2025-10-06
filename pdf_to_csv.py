import pdfplumber
import csv
import re
from datetime import datetime


def pdf_to_csv(pdf_path, csv_path):
    """
    Convert a race results PDF to a sorted CSV file.

    Args:
        pdf_path (str): Path to the input PDF file
        csv_path (str): Path where the sorted CSV will be saved
    """
    participants_data = []
    participants_list = []

    # Open PDF file and read its content
    with pdfplumber.open(pdf_path) as pdf:
        # Loop through each page in the PDF
        for page in pdf.pages:
            # Extract text from the page and split by line
            text = page.extract_text()
            if text:
                lines = text.split("\n")

                # Parse header information on the first page
                if page.page_number == 1:
                    competition_title = text[0]
                    competition_sponsor_info = text[1]
                    competition_date = text[2]
                    competition_type = text[3]
                    competition_header_data = text[5]

                competition_timekeeping_info = text[-3]
                competition_site = text[-2]

                if page.page_number == 1:
                    participants_data.extend(lines[6:-3])
                else:
                    participants_data.extend(lines[2:-3])

    # Extract participants data
    i = 0
    while i < len(participants_data):
        if participants_data[i] != "":
            # Split the participant's line data
            data = participants_data[i].split(" ")

            # Search for bad formatted data
            formatted_data = []
            for item in data:
                # Check if the element contains both letters and numbers
                match = re.match(r"([A-Za-zÀ-ÿá-úà-ùè-éî-ôù]+)(\d+)", item)
                if match:
                    name = match.group(1)
                    year = match.group(2)
                    formatted_data.append(name)
                    formatted_data.append(year)
                else:
                    formatted_data.append(item)
            data = formatted_data

            # Check if the data is complete (contains all required fields)
            if len(data) >= 5:
                # Extract participant data
                bib_number = data[0]
                race_time = data[-1]
                nationality = data[-2]
                sex = ""
                team = ""
                year = ""

                # Extract sex, team and year
                year_idx = next(
                    (
                        i
                        for i, w in enumerate(data[1:])
                        if re.match(r"^\d{4}$", w) or w.lower() == "null"
                    ),
                    None,
                )

                if year_idx is not None:
                    year = data[1:][year_idx]
                    if data[1:][year_idx + 1] == "M" or data[1:][year_idx + 1] == "F":
                        sex = data[1:][year_idx + 1]
                    athlete_name = " ".join(data[1:][:year_idx])
                    team = " ".join(data[1:][year_idx + 2 : -2])
                else:
                    year = "null"
                    sex = data[1:][-3]
                    athlete_name = " ".join(data[1:][1:-3])
                    team = ""

                # Check if next line continues the athlete name
                while (
                    i + 1 < len(participants_data)
                    and len(participants_data[i + 1].split()) < 5
                ):
                    next_line = participants_data[i + 1].strip()
                    athlete_name += " " + next_line
                    i += 1

                participants_list.append(
                    [
                        bib_number,
                        athlete_name.strip(),
                        year,
                        sex,
                        team,
                        nationality,
                        race_time,
                    ]
                )
                i += 1

    # Assemble competition metadata
    competition_metadata = {
        "title": competition_title,
        "sponsor": competition_sponsor_info,
        "date": competition_date,
        "type": competition_type,
        "header_data": competition_header_data,
        "timekeeping_info": competition_timekeeping_info,
        "site": competition_site,
    }

    # Sort participants list by race time
    participants_list.sort(key=lambda x: parse_race_time(x[6]))

    # Write sorted data to CSV file
    with open(csv_path, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)

        # Write header row with position column
        writer.writerow(
            [
                "pos",
                "pett",
                "athlete",
                "year",
                "sex",
                "team",
                "nat",
                "time",
            ]
        )

        # Write sorted data with positions
        for position, participant in enumerate(participants_list, 1):
            writer.writerow([position] + participant)

    return competition_metadata


def parse_race_time(time_str):
    """
    Parse a race time string into a datetime object for comparison.

    Args:
        time_str (str): Race time in format "HH:MM:SS"

    Returns:
        datetime: Parsed time or datetime.max for invalid times
    """
    try:
        return datetime.strptime(time_str, "%H:%M:%S")
    except ValueError:
        return datetime.max  # Return maximum datetime for invalid/missing times
