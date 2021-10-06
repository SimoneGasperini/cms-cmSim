from itertools import chain


DATALAKE_TO_COUNTRIES = \
    {
        'Switzerland':
        {
            'Switzerland'
        },

        'West Europe':
        {
            'Italy',
            'Spain',
            'Austria',
            'Germany',
            'United Kingdom',
            'Belgium',
            'Portugal',
            'France'
        },

        'East Europe':
        {
            'Finland',
            'Estonia',
            'Turkey',
            'Ukraine',
            'Hungary',
            'Poland',
            'Greece',
            'Russia'
        },

        'USA':
        {
            'USA'
        },

        'Brazil':
        {
            'Brazil'
        },

        'Asia':
        {
            'Taiwan',
            'South Korea',
            'India',
            'China',
            'Malaysia',
            'Pakistan',
            'Thailand'
        }
    }


countries = set(chain(*(DATALAKE_TO_COUNTRIES[datalake]
                        for datalake in DATALAKE_TO_COUNTRIES)))


COUNTRY_TO_DATALAKE = {country: datalake for country in countries
                       for datalake in DATALAKE_TO_COUNTRIES
                       if country in DATALAKE_TO_COUNTRIES[datalake]}
