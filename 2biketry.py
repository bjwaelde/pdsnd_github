import time
import pandas as pd
import numpy as np



CITY_DATA = { 'c': 'chicago.csv',
              'n': 'new_york_city.csv',
              'w': 'washington.csv' }
MONTHS = { '1': 'January',
           '2': 'February',
           '3': 'March',
           '4': 'April',
           '5': 'May',
           '6': 'June',
           '0': 'all months'  }
DAYS = { '1': 'Sunday',
         '2': 'Monday',
         '3': 'Tuesday',
         '4': 'Wednesday',
         '5': 'Thursday',
         '6': 'Friday',
         '7': 'Saturday',
         '0': 'all day'  }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter - can also use None (enter)
        (str) day - name of the day of week to filter by, or "all" to apply no day filter - can also use None (enter)
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    i = 1
    repeat = True
    while repeat:
        try:
            month = str(input('Please choose a month from January to June (0 for All, 1 for January, 2 for February, etc): ') or '0')
            # python's day number is Sunday = 0, Monday = 1. This is counter-intuitive for users. We will adjust it programatically.
            ## I learned the "or 0" from stackoverflow. Used it several times in this program.
            day = str(input('Please choose a day (0 for All, 1 for Sunday, 2 for Monday, etc): ') or '0')
            city = input('Please choose a city. C for Chicago, N for New York City, W for Washington: ')[0].lower()
            print('You have chosen to view data for {} on {} during {}'.format(CITY_DATA.get(city).split(".")[0].replace("_"," ").title(), DAYS.get(day)+'s', MONTHS.get(month)+""))
            city = CITY_DATA.get(city)
            # adjusting day programatically
            day = int(day)-1
            month = int(month)
        except:
            if i<2:
                print('Invalid input. Please check inputs and try again.')
                i+=1
            else:
                print('Multiple bad attempts. Terminating program.')
                break

        else:
            repeat = False
            print('-'*40)
            return city, month, day
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs


    # TO DO: get user input for month (all, january, february, ... , june)


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

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
    df = pd.read_csv(city)
    ## use index col = 0 to make the first column of csv the index column for df. I wanted to make it the index and name it, but never figured it out.
    ## can probably filter without adding the temporary columns
    df['StartTime'] =  pd.to_datetime(df['Start Time'])
    df['Start Day'] = df['StartTime'].dt.weekday
    df['Start Month'] = df['StartTime'].dt.month
    df['Start Hour'] = df['StartTime'].dt.hour
    if day != -1 and month != 0:
        df = df[(df['Start Day'] == day) & (df['Start Month'] == month)]
    elif day != -1 and month == 0:
        df = df[(df['Start Day'] == day)]
    elif day == -1 and month != 0:
        df = df[(df['Start Month'] == month)]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')


    # TO DO: display the most common month
    print('The most common month traveled is {}.\nThe most common day traveled is {}.\nThe most common hour that trips begin is {}{}.'.format(MONTHS.get(str(df[('Start Month')].mode()).split()[1]),DAYS.get(str(df[('Start Day')].mode()+1).split()[1]),str(df[('Start Hour')].mode()).split()[1],':00'))
    # TO DO: display the most common day of week
    # adjust the day number to take into account python's day numbering starts with Sunday = 0.



    # TO DO: display the most common start hour


    print('-'*40)
    del df['StartTime']
    del df['Start Hour']
    del df['Start Day']
    del df['Start Month']
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')


    # TO DO: display most commonly used start station
    print('The most common starting station is {}'.format(str(df[('Start Station')].mode()).split(" ",1)[1].strip().replace("dtype: object","")))

    # TO DO: display most commonly used end station
    print('The most common ending station is {}'.format(str(df[('End Station')].mode()).split(" ",1)[1].strip().replace("dtype: object","")))

    # TO DO: display most frequent combination of start station and end station trip
    ## i learned the "to frames" and "to strings" and "reset index" from stackoverflow as well. Using it multiple times in program to clean up output.
    print('Below is the most popular trip:\n')
    df1 = df.groupby(['Start Station', 'End Station']).size().to_frame(name = 'Trips').reset_index()
    df1 = df1.sort_values(by ='Trips', ascending=False)
    print(df1.head(1).to_string(index=False))

    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')

    ##print(df.columns)
    # TO DO: display total travel time
    print('Total travel time: {} hours and {} minutes'.format(int(df['Trip Duration'].sum()//3600), int((df['Trip Duration'].sum() % 3600)//60)))
    # TO DO: display mean travel time
    print('Mean travel time was: {} minutes and {} seconds'.format(int(df['Trip Duration'].mean()//60), int((df['Trip Duration'].sum() % 60))))


    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')

    print('Bikeshare Users by User Type:\n')
    # TO DO: Display counts of user types
    print(df['User Type'].value_counts().to_frame())
    ##df['User Type'].plot(kind='bar')
    print('\n')


    for i in range(1):
        try:
    # TO DO: Display counts of gender
            df['Gender'].fillna('Unspecified', inplace = True)
            print('Bikeshare Users by Gender:\n')
            print(df['Gender'].value_counts().to_frame())
            print('\n')
            print('Gender Breakdown by User Type:\n')
            df2 = df.groupby(['User Type', 'Gender']).size().to_frame(name = 'Trips').reset_index()
            df2 = df2.sort_values(by =['User Type','Trips'], ascending=False)
            print(df2.to_string(index=False))
            print('\n')
            print('Birth Year statistics:\n')
            year_dict = dict(df['Birth Year'].describe())
            print('The youngest bikeshare user was born in: {}'.format(int(year_dict.get('max'))))
            print('The oldest bikeshare user was born in: {}'.format(int(year_dict.get('min'))))
            print('The most common year of birth for users is: {}'.format(int(year_dict.get('mean'))))

    # TO DO: Display earliest, most recent, and most common year of birth
        except:
            print('Gender and birth year are not available for bikeshare users in the chosen city')
            break
        finally:

            print('-'*40)

def view_raw(df):
    """checks to see if the user wants to view the raw data, and if so, optimizes for viewing. Allows user to see 5 rows at a time. Gives the user multiple chances to correct incorrect inputs"""


    i = 1
    ## now that I know about using OR statements to handle nulls, I would write this differently.
    viewing = input('Would you like to view the raw data? Y or N: ') or 's'
    while True:
        try:
            if viewing[0].lower() =='n':
              ##  print('nope nope nope')
                break
            if i == 2:
                break
        except:
            viewing = input('Invalid entry. Would you like to view the raw data? Y or N: ')
            i+=1
            if i == 2:
                viewing ='n'

        else:
            if viewing[0].lower() =='y':
                break
            else:
                viewing = input('Invalid entry. Would you like to view the raw data? Y or N: ') or 's'
                i+=1
    if viewing[0].lower() == 'y':
        df.rename( columns={'Unnamed: 0':'Trip ID'}, inplace=True )
        df = df.sort_values(by =['Trip ID'], ascending=True)
        df = df.reset_index(drop=True)
        a = 0
        z = 5
        ## learned these 3 display commands from stackoverflow
        pd.set_option('display.width',150)
        pd.set_option('display.max_columns', None)
        pd.options.display.float_format = '{:.0f}'.format

    while viewing[0].lower() == 'y':
        try:
            print(df[a:z])
            a+=5
            z+=5
            viewing = input('Would you like to see more raw data? Y or N: ') or 'n'
            ##print(viewing)
        except:
            print('this is the exception')
def main():
    restart = 'y'
    while restart[0].lower() == 'y':
        try:
            city, month, day = get_filters()
            df = load_data(city, month, day)
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            view_raw(df)
            restart = input('Do you want to start again? Y to restart: ') or 'n'
            ## At this point, it's ok for the program just to exit if it does not get yes.  or is used to avoid a crash if the entry is null.
            print('\n')
        except:
            break
if __name__ == "__main__":
	main()
