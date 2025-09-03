# Mobi Bike Data Analysis

This project will gather and analyze Mobi Bike data from Mobi by Rogers [System data](https://www.mobibikes.ca/en/system-data), 
to identify usage patterns for stations and bike types over different timeframes. I have limited the timeframe to 2024, because it is the most recent and reading speeds will not be affected.
The analysis focuses on:
- Which stations are the most used during a particular time
    - Busiest Station during Rush Hour
        - (defined as 7:00 am - 10:00 am and 3:00 pm to 6:00 pm)
    - Busiest Station each Month
    - Busiest Station each Week 
- Which bike was most used, and the average distance covered?
    - Based on the data, can an obvious distinction between bike type and distance be seen?
        - Regular bike and short commute
        - Electric bike and short commute
        - Regular bike and long commute
        - Electric bike and long commute
    - Along with the above, is there an increase in average speed with the use of electric bikes?

## Requirements 
pip install -r requirements.txt

## Example Analysis of the System Data for 2024
Most used station during rush hour. 
- Departure: Stanley Park - Information Booth, 
- Return: Stanley Park - Information Booth
Busiest station per Week. 
- Departure: Stanley Park - Information Booth, 
- Return: Stanley Park - Information Booth
Busiest station per Month. 
- Departure: Stanley Park - Information Booth, 
- Return: Stanley Park - Information Booth
**Stanley Park - Information Booth** being in each section is not an error but the most used station.

## 1. Data Gathering

The first step is to retrieve the latest Mobi Bike dataset using:

```bash
    python3 GatherData.py [List Limit]
```
Where [List Limit] is the number of dataset, from recent to past, you would want. Default = 100

Months that have to be manually downloaded are **'February_2024', 'August_2023'**


## 2. Data Analysis

Once the data is gathered, an analysis can begin, run:
```bash
    python AnalyzeData.py Mobi_Data_csv
```
Mobi_Data_(csv,gzip,lz4) will hold the dataset receptively to their compression