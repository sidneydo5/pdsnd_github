import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Please input a city (Chicago, New York City or Washington) to display data from: ''').lower()
        if city in CITY_DATA.keys():
            break
        else:
            print('\nSorry, you typed an incorrect city. Please enter Chicago, New York City or Washington to display your data.\n')
            continue

    # get user input for month (all, january, february, ... , december)
    while True:
        month = input('Please input a month to retrieve data for. You may type any month of of the calendar year. Or just type all to not use a month filter. ''').lower()
        months = ['january','february','march','april','may','june','july','august','september','october','november','december']
        if month in months:
            print('\nLet\'s pull up data for the month you selected: ''')
            break
        elif month == 'all':
            print('\nAlright, let\'s check the data for all the months!')
            break
        else:
            print('\nSorry, you made an invalid entry. Please try again.')
            continue

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Now, please select a weekday name to filter by. Or type all to search all days. ''').lower()
        days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        if day in days:
            print('\nLet\'s pull up data for the day you selected: ''')
            break
        elif day == 'all':
            print('\nAlright, let\'s check the data for all the days of the week!')
            break
        else:
            print('\nSorry, you made an invalid entry. Please try again.')
            continue

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

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract hour, month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month_name()
    df['Day_of_week'] = df['Start Time'].dt.day_name()
    df['Hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['Month'].str.contains(month.title())]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['Day_of_week'].str.contains(day.title())]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['Month'].mode()[0]
    print('The most common month was {}.'.format(popular_month))

    # display the most common day of week
    popular_day = df['Day_of_week'].mode()[0]
    print('The most common day of the week was {}.'.format(popular_day))

    # display the most common start hour
    popular_start_hour = df['Hour'].mode()[0]
    print('The most common start hour was {}.'.format(popular_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('The most common start station was {}.'.format(most_common_start_station))

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('The most common end station was {}.'.format(most_common_end_station))

    # display most frequent combination of start station and end station trip
    combo_stations = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False)
    print('The most frequent combination of start and end stations were {}.'.format(combo_stations))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time was {} seconds.'.format(total_travel_time))

    # display mean travel time
    avg_travel_time = df['Trip Duration'].mean()
    print('The average travel time was {} seconds.'.format(avg_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The count of customer and subscriber user types were: {}.'.format(user_types))

    # Display counts of gender
    if 'Gender' in df:
        genders = df['Gender'].value_counts()
        print('The gender counts of users were: {}.'.format(genders))
    else:
        print('Gender stats cannot be calculated because Gender data does not exist in the dataset.')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_birth_year = df['Birth Year'].min()
        print('The earliest birth year of users were: {}.'.format(int(earliest_birth_year)))
        latest_birth_year = df['Birth Year'].max()
        print('The most recent birth year of users were: {}.'.format(int(latest_birth_year)))
        most_common_birth_year = df['Birth Year'].mode()[0]
        print('The most common birth year of users were: {}.'.format(int(most_common_birth_year)))
    else:
        print('Birth Year stats cannot be calculated because Birth Year data does not exist in the dataset.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """Displays the raw dataset to the user 5 rows at a time. Based on their input, 5 more rows at a time can be accessed."""
    view_data = input('Would you like to view 5 rows of individual trip data? Enter yes or no? ''').lower()
    start_loc = 0
    while (view_data == 'yes'):
        print(df.iloc[start_loc:start_loc +5])
        start_loc += 5
        view_display = input('Do you wish to continue and view another 5 rows of data?: ').lower()
        if view_display.lower() != 'yes':
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
