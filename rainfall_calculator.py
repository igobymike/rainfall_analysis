"""
Michael Birklett
6/4/2024
rainfall_calculator.py
This program will allow users to input the name of a file containing rainfall data and output statistics about the rainfall
data. The program will process the input data by omitting negative value records and will stop processing the data
if/when it detects the sentinel value +99999
"""
import io


#checks entries throughout the program for emtpy string entries. repeats the question if input == False
def entry_validation(prompt):
    while True:
        entry = str(input(prompt))
        if not bool(entry and entry.strip()):
            print("Invalid entry. Try again.")
        else:
            return entry


#function takes in the name of the input file and the name of the output file from the user then returns them
def get_user_input():
    # user enters input file name and location
    input_file_path = entry_validation("\nPlease enter the path where your data file is located:")
    input_file_name = entry_validation("Please enter the name of your text file:")
    input_file_path = file_path_check(input_file_path)
    input_file_name = extension_check(input_file_name)

    #concatenates entries
    input_file = input_file_path + input_file_name

    while True:
        x = int(input("\nWould you like the cleansed data file saved to the same location as your input file.\n1 = "
                      "YES | 2 = NO "))

        if x == 1:
            # user enters output file name only
            output_file_path = input_file_path
            output_file_name = entry_validation("\nPlease enter the name that you would like me to give to the "
                                                "processed data file:")
            output_file_name = extension_check(output_file_name)

            # concatenates entries
            output_file = output_file_path + output_file_name
            break

        elif x == 2:
            # user enters output file name and location
            output_file_path = entry_validation("Please enter the path where you would like me to store your cleansed data:")
            output_file_name = entry_validation("Please enter the name of the cleansed data file:")
            output_file_path = file_path_check(output_file_path)
            output_file_name = extension_check(output_file_name)

            # concatenates entries
            output_file = output_file_path + output_file_name
            break

        else:
            print("Invalid entry. Please enter 1 or 2.\n ")

    return input_file, output_file

#checks if user provided the backslash in their entry
def file_path_check(_):
    if _.endswith("\\"):
        return _
    else:
        _ += "\\"
        return _


#checks if the user provided the .txt file extension in their entry
def extension_check(_):

    if _.endswith(".txt"):
        return _
    else:
        _ += ".txt"
        return str(_)


#function takes in the location and name of the input file, opens the file if possible, transfers the lines into a list
#then returns the list (no business logic performed)
def get_input_data(input_file):
    input_list = []
    rows_read = 0
    try:
        with io.open(input_file,'r') as file:
            for line in file:                            #iterates over each row in file
                rows_read += 1                           # counts the total number of rows read
                line = line.strip()                      #strips each line down removing spaces
                if line == "99999":                        # if sentinel value encountered  break
                    break
                else:
                    input_list.append(line)               #append to list if positive float
        return None, input_list, rows_read

    except Exception as e:
        print(f"\nException: {e}\n")
        while True:
            retry = int(input("Would you like to start over and re-enter input file details?\n1 = YES | 2 = NO  "))
            if retry == 2:
                return 2, None, None
            elif retry == 1:
                return 1, None, None
            else:
                print("Invalid Entry. Please enter 1 or 2.")


#function takes the list then returns a new list based on the business logic (no negative numbers and stops at sentinel
def process_data(input_list):
    processed_list = []
    good_rows = 0

    for element in input_list:                            # iterates over  each element in the list
        try:                                              # checks to see if the line is a digit
            element = float(element)                       # if it's a digit, convert it to a float
            if element < 0:                                # if less than 0 (neg number) pass
                pass
            elif element >= 0:
                good_rows += 1                             # counts the number of good rows
                processed_list.append(element)             # append to list if positive float
        except ValueError:
            pass                                            # pass on non digit lines

    return processed_list, good_rows


#function performs statistical analysis on "good" rows from process_data() list
def output_information(processed_list, rows_read, good_rows):
    count_rain_days = 0
    sum_rain_days = 0


    for x in processed_list:
        if x > 0:
            count_rain_days +=1

    for x in processed_list:
        if x > 0:
            sum_rain_days += x

    min_value = min(processed_list)
    max_value = max(processed_list)
    average_rain_all = good_rows/ sum(processed_list)
    average_rain_lim = count_rain_days / sum_rain_days

    print("\n")
    print("-" * 40)
    print(f"The total number of rows read : {rows_read}")
    print(f"The total number of good rows : {good_rows}")
    print("-" * 40)
    print("\nStatistical Findings:")
    print(f"The minimum value found within the good rows: {min_value:.5f} ")
    print(f"The maximum value found within the good rows: {max_value:.5f} ")
    print(f"The average rainfall value inclusive of rows that contain only zeros: {average_rain_all:.5f} ")
    print(f"The average rainfall value exclusive of rows that contain only zeros: {average_rain_lim:.5f} ")

#receives the good rows from proces_data() then outputs them to a file
def save_file(processed_list, output_file):

    with open(output_file, 'w') as file:
        for element in processed_list:
            file.write(f"{element}\n")
    print("-" * 40)
    print ("\nAll done! I've saved your processed data file here:")
    print(output_file)
    print("-" * 40)

def main(cleansed=None):
    print("\nHi! So you're interested in gathering statistical details about your rainfall data. I can help with "
          "that!\n"
          "I can provide you with details about your data including min/max rainfall amounts and rainfall averages.\n"
          "I'll even cleanse the data and place the cleansed data into a file of your choosing!\n"
          "All I need is the the name and location of your data file and the name of the cleansed data file that I "
          "can create for you.")
    while True:
        input_file, output_file = get_user_input()
        retry, input_list, rows_read = get_input_data(input_file)

        #checks if user would like to retry entering the file path again
        if retry == 2:
            print("Goodbye!")
            return
        elif retry == 1:
            continue
        else:
            processed_list, good_rows = process_data(input_list)
            output_information(processed_list, rows_read, good_rows)
            save_file(processed_list, output_file)

        x = int(input("\nDo you have another file that you would like me to process?.\n1 = "
                      "YES | 2 = NO "))
        if x == 2:
            print("Goodbye!")
            return

if __name__ == "__main__":
    main()
