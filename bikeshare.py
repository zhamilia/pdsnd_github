

import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
CITY_DATA['new york']='new_york_city.csv'
cities=CITY_DATA.keys()
months = ['january', 'february', 'march', 'april', 'may', 'june']
day_of_week=['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    while True:
        #check the city
        city=str(input('\nPlease select the city to explore: Chicago, New York, Washington\n ')).lower()
        if city not in cities:
            print('Incorrect Value! Type Chicago, New York or Washington\n')
            continue
        #if city is ok
        else:
            while True:
                #check the filter
                fil=str(input('\nHow would you like to filter the data (by month, day, both or not at all (type none))?\n ')).lower()

                if fil=='day':
                    month='all'

                    while True:
                    #check the day
                        day=str(input('Please enter the day (All, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday)\n')).lower()
                        if day!='all' and day not in day_of_week:
                            print('Please enter the day correctly\n')
                            continue
                        break


                elif fil=='month':
                        day='all'
                        while True:
                        #check the month
                            month=str(input('Please enter the month (All, January, February, March, April, May, June)\n')).lower()
                            if month!='all' and month not in months:
                                print('Please enter the month correctly\n')
                                continue
                            break

                elif fil=='both':
                        while True:
                        #check the month
                            month=str(input('Please enter the month (All, January, February, March, April, May, June)\n')).lower()
                            if month!='all' and month not in months:
                                print('Please enter the month correctly\n')
                                continue
                            break

                        while True:
                        #check the day
                            day=str(input('Please enter the day (All, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday)\n')).lower()
                            if day!='all' and day not in day_of_week:
                                    print('Please enter the day correctly\n')
                                    continue
                            break



                elif fil=='none':

                        month='all'
                        day='all'

                else:

                    print('\nPlease enter day, month or both\n')
                    continue
                break
        break
    return (city, month, day);

def load_data(city,month, day):
        """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
        df = pd.read_csv(CITY_DATA[city])
        df['Start Time'] =pd.to_datetime(df['Start Time'])
        df['month'] = df['Start Time'].dt.month
        df['day_of_week'] = df['Start Time'].dt.weekday_name
        if month != 'all':
            months = ['january', 'february', 'march', 'april', 'may', 'june']
            month = months.index(month) + 1
            df = df[df['month'] == month]
        if day != 'all':
            df = df[df['day_of_week']==day.title()]
        return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    freq_mon = df['month'].value_counts().idxmax()
    freq_dow = df['day_of_week'].value_counts().idxmax()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    freq_hour = df['hour'].value_counts().idxmax()

    print("\nThe most common hour is: ",freq_hour)
    print("\nThe most common month is: ",freq_mon)
    print("\nThe most common day of week is: ",freq_dow)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    freq_sst = df['Start Station'].value_counts().idxmax()
    freq_est = df['End Station'].value_counts().idxmax()
    combo1=df['Start Station'].astype(str)+" TO "+df['End Station'].astype(str)
    combo2=combo1.describe()['top']

    print("\nThe most commonly used start station is: ",freq_sst)
    print("\nThe most commonly used end station is: ",freq_est)
    print("\nThe most frequent combination of start station and end station trip is: ",combo2)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    avg_td=df['Trip Duration'].describe()["mean"]
    total_td=df['Trip Duration'].sum()

    print("\nThe mean travel time is (in seconds): ",avg_td)
    print("\nThe total travel time is (in seconds): ",total_td)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    user_types_sub=df['User Type'].value_counts()['Subscriber']
    user_types_cus=df['User Type'].value_counts()['Customer']

    try:

        user_types_mal=df['Gender'].value_counts()['Male']
        user_types_fem=df['Gender'].value_counts()['Female']
        yob_min=df['Birth Year'].describe()["min"]
        yob_max=df['Birth Year'].describe()["max"]
        yob_freq=df['Birth Year'].value_counts().idxmax()
        print("\nMale: ",user_types_mal)
        print("\nFemale: ",user_types_fem)
        print("\nEarliest year of birth: ",yob_min)
        print("\nMost recent year of birth: ",yob_max)
        print("\nMost common year of birth: ",yob_freq)
        print("\nNumber of subscribers is: ",user_types_sub)
        print("\nNumber of customers is: ",user_types_cus)
        print("\nThis took %s seconds." % (time.time() - start_time))

    except KeyError:
        print("We don't have information about gender and year of birth for this city")

        print("\nNumber of subscribers is: ",user_types_sub)
        print("\nNumber of customers is: ",user_types_cus)

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
def display_data(df):
    start=0
    for i in range (0,df.shape[0]):

        if start<5:
            print (df.iloc[i])
            start=start+1

        else:
            start=0
            sel=str(input("Do you want to see raw data?")).lower()
            if sel=='yes':
                continue
            else:
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
