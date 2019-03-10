import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#defining list to store the applicable months
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

#defining list to store the days of a week
days_of_week = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city
    while True:
        try:
            city = str(input("Please enter the city name: ")).lower()
            if city not in CITY_DATA.keys():
                print("Currently we have data available only for {}. Please choose either of these to proceed further.".format([key for key in CITY_DATA.keys()]))
            else:
                break
        except (ValueError, KeyboardInterrupt):
            print("Please enter a valid city name.")

    # Get user input for month
    while True:
        try:
            month = str(input("Please enter the month: ")).lower()
            if month not in months:
                print("Please choose from the list of available months {}".format(months))
            else:
                break
        except (ValueError, KeyboardInterrupt):
            print("Please enter a valid month.")

    # Get user input for day of week
    while True:
        try:
            day = str(input("Please enter the day of week: ")).lower()
            if day not in days_of_week:
                print("The input is not a valid day of the week. Please choose one of the {}".format(days_of_week))
            else:
                break
        except (ValueError, KeyboardInterrupt):
            print("Please enter a valid day.")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    if 'Start Time' in df.columns:
    # convert the Start Time column to datetime
        df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
        df['month'] = df['Start Time'].dt.month
        df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if 'month' in df.columns:
        print("Most common month: {}".format(df['month'].mode()[0]))

    # display the most common day of week
    if 'day_of_week' in df.columns:
        print("Most common month: {}".format(df['day_of_week'].mode()[0]))

    # display the most common start hour
    if 'Start Time' in df.columns:
        df['hour'] = df['Start Time'].dt.hour
        print("Most common hour: {}".format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    if 'Start Station' in df.columns:
        print("Most common start station: {}".format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    if 'End Station' in df.columns:
        print("Most common end station: {}".format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    if 'Start Station' in df.columns and 'End Station' in df.columns:
        df['Frequent Comb Station'] = df['Start Station'] + ', ' + df['End Station']
        print("Most common combination of start and end station: {}".format(df['Frequent Comb Station'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    if 'Trip Duration' in df.columns:
        print("Total travel time: {}".format(df['Trip Duration'].sum()))
    # display mean travel time
        print("Average travel time: {}".format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if 'User Type' in df.columns:
        print("Counts of different user types: {}".format(df['User Type'].value_counts(dropna=True)))

    # Display counts of gender
    if 'Gender' in df.columns:
        print("Counts of different gender: {}".format(df['Gender'].value_counts(dropna=True)))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print("Most earliest year of birth: {}".format(df['Birth Year'].min()))
        print("Most recent year of birth: {}".format(df['Birth Year'].max()))
        print("Most common year of birth: {}".format(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        #prompt the user to ask if they would like to see raw data. if yes display 5 rows per input
        row_count = 0
        while True:
            rawinput = input('\nWould you like to see the raw data? Enter yes or no.\n').lower()
            if rawinput == 'yes':
                print(df[row_count:row_count+5])
                row_count += 5
            else:
                break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
