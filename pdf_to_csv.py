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
    participants_list = []  # Temporary list to store all participants data

    # Open PDF file and read its content
    with pdfplumber.open(pdf_path) as pdf:
        # Loop through each page in the PDF
        for page in pdf.pages:
            # Extract text from the page and split by line
            text = page.extract_text()
            text = text.split("\n")
            # print(text)

            # Parse header information on the first page
            if page.page_number == 1:
                competition_title = text[0]
                competition_sponsor_info = text[1]
                competition_date = text[2]
                competition_type = text[3]
                competition_header_data = text[5]
                participants_data = text[6:-3]
            else:
                participants_data = text[2:-3]

            competition_timekeeping_info = text[-3]
            competition_site = text[-2]

            # Extract participants data
            i = 0
            while i < len(participants_data):
                # print(participants_data[i])
                if participants_data[i] != "":
                    # Split the participant's line data
                    data = participants_data[i].split(" ")
                    # print(data)

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
                        team = ""
                        year = ""

                        # Extract the team name and year from the middle part of the data
                        for word in reversed(
                            data[:-2]
                        ):  # Exclude the last two elements
                            if word.isdigit() or word == "null":
                                year = word
                                break
                            team = word + " " + team
                        team = team[:-1]  # Remove the trailing space

                        athlete_name = " ".join(
                            data[1 : data.index(year)]
                        )  # Join the name parts

                    # Check for name continuation in the next line
                    if i < len(participants_data) - 1:
                        next_data = participants_data[i + 1].split(" ")

                    # If next line is a continuation of the current participant's name
                    if len(next_data) < 5:
                        athlete_name += " " + " ".join(next_data[:])
                        i += 1  # Skip the next line as it's part of current name
                    i += 1

                    # Add participant data to the temporary list
                    participants_list.append(
                        [bib_number, athlete_name, year, team, nationality, race_time]
                    )

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
    participants_list.sort(key=lambda x: parse_race_time(x[5]))

    # Write sorted data to CSV file
    with open(csv_path, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)

        # Write header row with position column
        writer.writerow(
            [
                "position",
                "bib number",
                "athlete",
                "year",
                "team",
                "nationality",
                "race time",
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
