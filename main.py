import csv
import numpy as np
import matplotlib.pyplot as plt

prompt = "> "


class Site_Forecast():

    def __init__(self):
        # List of rows from the WinData.csv. (All the rows.)
        self.data = self.__get_data()
        # The number of measurements is equal to the len of the data list.
        self.number_of_rows = len(self.data)

        # Key-value mapping: day -> maximum speed (14.11.2021 -> 7.9)
        self.maximum_speed_per_day = {}
        # Populates the maximum_speed_per_day dictionary.
        self.__get_maximum_speed_per_day()

        # Maximum speed for the full period.
        self.maximum_speed = self.__get_maximum_speed()

        # List of rows from the WinData.csv which have the wind speed between 2.5 and 25. (Filtered rows.)
        self.filtered_data = self.__get_data([2.5, 25])

        # Key-value mapping between the wind direction and a list of wind degrees specific to that wind direction.
        self.wind_degree_sorted_by_wind_direction = {
            "E": [],
            "S": [],
            "W": [],
            "N": []
        }
        # Populates wind_degree_sorted_by_wind_direction.
        self.__sort_wind_degree_by_wind_direction()

        # List of key-value mappings of form: timestamp -> wind direction (14.11.2021 -> E)
        self.timestamp_sorted_by_wind_direction = []
        # Populates timestamp_sorted_by_wind_direction.
        self.__sort_timestamp_by_wind_direction()

        # Stores the number of measurements per day.
        self.days_occurrence = {}
        # Counts the number of measurements for each idividual day.
        self.__count_measurements_by_day()

        # Key-value mapping between the wind direction and a list of wind speeds specific to that wind direction.
        self.wind_speed_sorted_by_wind_direction = {
            "E": [],
            "S": [],
            "W": [],
            "N": []
        }
        # Populates wind_speed_sorted_by_wind_direction.
        self.__sort_wind_speed_by_wind_direction()

    def __get_data(self, interval=None):
        rows = []

        with open('WindData.csv', 'r') as csv_file:
            file_reader = csv.DictReader(csv_file, delimiter=";")

            for row in file_reader:
                # If an interval is given, store only the rows which are in that interval...
                if interval is not None:
                    speed = float(row['WindSpeed'].replace(",", "."))
                    if interval[0] <= speed <= interval[1]:
                        rows.append(row)
                    else:
                        continue
                # Otherwise, store everything from the file.
                else:
                    rows.append(row)

        return rows

    def __count_measurements_by_day(self):
        days = []

        # Get all the available dates (only day) from the file.
        for data in self.data:
            day = data["ï»¿Timestamp"].split(" ")[0]
            if day not in days:
                days.append(day)

        # Counts the number of appearances in the WinData.csv for each day.
        for day in days:
            for data in self.data:
                day_in_data = data["ï»¿Timestamp"].split(" ")[0]
                if day == day_in_data:
                    if day not in self.days_occurrence:
                        self.days_occurrence.update({day: 0})
                    self.days_occurrence[day] = self.days_occurrence[day] + 1

    def __get_maximum_speed_per_day(self):
        for row in self.data:
            values = list(row.values())
            values[0] = values[0].split(' ')[0]

            day = values[0]
            speed = values[2]

            # If the day is not in the dictionary yet...
            if day not in self.maximum_speed_per_day:
                self.maximum_speed_per_day.update({day: []})

            # For that day I am adding the speed.
            self.maximum_speed_per_day[day].append(float(speed.replace(",", ".")))

        # Keep only the maximum speed form the list above...
        for day in self.maximum_speed_per_day:
            self.maximum_speed_per_day[day] = max(self.maximum_speed_per_day[day])

    def __get_maximum_speed(self):
        speeds = list(self.maximum_speed_per_day.values())
        return max(speeds)

    def __sort_wind_degree_by_wind_direction(self):
        for row in self.filtered_data:
            wind_direction = int(row['WindDirection'])

            if 45 < wind_direction < 135:
                self.wind_degree_sorted_by_wind_direction["E"].append(wind_direction)
            if 135 < wind_direction < 225:
                self.wind_degree_sorted_by_wind_direction["S"].append(wind_direction)
            if 225 < wind_direction < 315:
                self.wind_degree_sorted_by_wind_direction["W"].append(wind_direction)
            if (315 < wind_direction < 360) or (1 < wind_direction < 45):
                self.wind_degree_sorted_by_wind_direction["N"].append(wind_direction)

    def plot_wind_degree_by_wind_direction(self):
        bar_width = 0.25
        # Set figure size.
        fig = plt.subplots(figsize=(12, 8))

        averages_of_wind_speeds_for_directions = [sum(self.wind_degree_sorted_by_wind_direction["E"]) / len(self.wind_degree_sorted_by_wind_direction["E"]),
                                                  sum(self.wind_degree_sorted_by_wind_direction["S"]) / len(self.wind_degree_sorted_by_wind_direction["S"]),
                                                  sum(self.wind_degree_sorted_by_wind_direction["W"]) / len(self.wind_degree_sorted_by_wind_direction["W"]),
                                                  sum(self.wind_degree_sorted_by_wind_direction["N"]) / len(self.wind_degree_sorted_by_wind_direction["N"])]

        # Return evenly spaced values within a given interval.
        # 4 -> 0 1 2 3
        br1 = np.arange(len(averages_of_wind_speeds_for_directions))

        # X -> br1
        # Y -> averages_of_wind_speeds_for_directions
        plt.bar(br1, averages_of_wind_speeds_for_directions, color='g', width=bar_width,
                edgecolor='grey', label='AVERAGE WIND DEGREE')

        plt.ylabel('WIND DEGREE', fontweight='bold', fontsize=15)
        plt.xlabel('WIND DIRECTION', fontweight='bold', fontsize=15)
        plt.xticks([r for r in range(len(averages_of_wind_speeds_for_directions))],
                   ['E', 'S', 'W', 'N'])

        plt.legend()
        plt.show()

    def plot_frequency_for_each_wind_direction(self):
        bar_width = 0.25
        fig = plt.subplots(figsize=(12, 8))

        number_of_data_points = [len(self.wind_degree_sorted_by_wind_direction["E"]),
                                 len(self.wind_degree_sorted_by_wind_direction["S"]),
                                 len(self.wind_degree_sorted_by_wind_direction["W"]),
                                 len(self.wind_degree_sorted_by_wind_direction["N"])]

        br1 = np.arange(len(number_of_data_points))

        plt.bar(br1, number_of_data_points, color='r', width=bar_width,
                edgecolor='grey', label='NUMBER OF DATA POINTS')

        plt.ylabel('FREQUENCY', fontweight='bold', fontsize=15)
        plt.xlabel('WIND DIRECTION', fontweight='bold', fontsize=15)
        plt.xticks([r for r in range(len(number_of_data_points))],
                   ['E', 'S', 'W', 'N'])

        plt.legend()
        plt.show()

    def __sort_timestamp_by_wind_direction(self):
        for row in self.filtered_data:
            wind_direction = int(row['WindDirection'])
            timestamp = row['ï»¿Timestamp'].replace(",", ".")

            if 45 < wind_direction < 135:
                self.timestamp_sorted_by_wind_direction.append({timestamp: "E"})
            if 135 < wind_direction < 225:
                self.timestamp_sorted_by_wind_direction.append({timestamp: "S"})
            if 225 < wind_direction < 315:
                self.timestamp_sorted_by_wind_direction.append({timestamp: "W"})
            if (315 < wind_direction < 360) or (1 < wind_direction < 45):
                self.timestamp_sorted_by_wind_direction.append({timestamp: "N"})

    def plot_timestamp_by_wind_direction(self):
        x = []
        y = []
        for element in self.timestamp_sorted_by_wind_direction:
            for key, value in element.items():
                x.append(key)
                y.append(value)

        plt.scatter(x, y, c="blue")

        # To show the plot
        plt.show()

    def __sort_wind_speed_by_wind_direction(self):
        for row in self.filtered_data:
            wind_direction = int(row['WindDirection'])
            wind_speed = (float(row["WindSpeed"].replace(",", ".")))

            if 45 < wind_direction < 135:
                self.wind_speed_sorted_by_wind_direction["E"].append(wind_speed)
            if 135 < wind_direction < 225:
                self.wind_speed_sorted_by_wind_direction["S"].append(wind_speed)
            if 225 < wind_direction < 315:
                self.wind_speed_sorted_by_wind_direction["W"].append(wind_speed)
            if (315 < wind_direction < 360) or (1 < wind_direction < 45):
                self.wind_speed_sorted_by_wind_direction["N"].append(wind_speed)

    def plot_wind_speed_by_wind_direction(self):
        bar_width = 0.25
        fig = plt.subplots(figsize=(12, 8))

        averages_of_wind_speeds_for_directions = [sum(self.wind_speed_sorted_by_wind_direction["E"]) / len(self.wind_speed_sorted_by_wind_direction["E"]),
                                                  sum(self.wind_speed_sorted_by_wind_direction["S"]) / len(self.wind_speed_sorted_by_wind_direction["S"]),
                                                  sum(self.wind_speed_sorted_by_wind_direction["W"]) / len(self.wind_speed_sorted_by_wind_direction["W"]),
                                                  sum(self.wind_speed_sorted_by_wind_direction["N"]) / len(self.wind_speed_sorted_by_wind_direction["N"])]

        br1 = np.arange(len(averages_of_wind_speeds_for_directions))

        plt.bar(br1, averages_of_wind_speeds_for_directions, color='c', width=bar_width,
                edgecolor='grey', label='AVERAGE WIND SPEED')

        plt.ylabel('WIND SPEED', fontweight='bold', fontsize=15)
        plt.xlabel('WIND DIRECTION', fontweight='bold', fontsize=15)
        plt.xticks([r for r in range(len(averages_of_wind_speeds_for_directions))],
                   ['E', 'S', 'W', 'N'])

        plt.legend()
        plt.show()


def menu():
    print("Hi and welcome to SITE Forecast module\n Please enter a number in order to select the option")
    print("1.Display date interval and number of measurements")
    print("2.Display the maximum speed for each day and the full period")
    print("3.Plot graph of frequency for each wind direction")
    print("4.Plot graph of average wind degree for each wind direction")
    print("5.Plot graph of wind speed for each wind direction")
    print("6.Plot graph of wind direction per date")
    print("Press Q to Quit")
    option = input(prompt)
    return option


if __name__ == '__main__':
    sp = Site_Forecast()

    option = menu()
    while option.lower() != "q":
        if option == "1":
            print(f"Number of measurements: {sp.number_of_rows}.")
            print("Number of measurements per day:\n")
            for key, value in sp.days_occurrence.items():
                print(f"- {key}: {value}\n")
        elif option == "2":
            print(f"Maximum speed: {sp.maximum_speed}.")
            print("Maximum speed per day:\n")
            for key, value in sp.maximum_speed_per_day.items():
                print(f"- {key}: {value}\n")
        elif option == "3":
            sp.plot_frequency_for_each_wind_direction()
        elif option == "4":
            sp.plot_wind_degree_by_wind_direction()
        elif option == "5":
            sp.plot_wind_speed_by_wind_direction()
        elif option == "6":
            sp.plot_timestamp_by_wind_direction()

        option = menu()
