import pandas as pd
from pathlib import Path
import os, sys

def main():
    parentdir = Path(__file__).parents[1]
    sys.path.append(parentdir)
    file_path = os.path.join(parentdir,'data', 'final.txt')

    data = pd.read_csv(file_path, header=None,usecols=[1,2,8], dtype='str')

    data = data.dropna()
    data.columns = ['start', 'end', 'zipcode']

    data['start'] = pd.to_datetime(data['start'], format=r"%m/%d/%Y %H:%M:%S %p")
    data['end'] = pd.to_datetime(data['end'], format=r"%m/%d/%Y %H:%M:%S %p")
    data['month'] = data['end'].dt.month
    data['diff_hours'] = round((data['end']-data['start']).dt.total_seconds()/3600.0,4)

    data = data[data['diff_hours'] >= 0]

    grouped=data.groupby(['zipcode','month'], as_index=False)['diff_hours'].mean()
    final=grouped.pivot(index='month',columns='zipcode')
    final.columns = final.columns.droplevel(0)

    avg_grouped = data.groupby(['month'])['diff_hours'].mean()

    avg_grouped.to_csv(os.path.join(parentdir,'data', 'nyc_avg.csv'))
    final.to_csv(os.path.join(parentdir,'data', 'nyc_grouped.csv'))


if __name__ == '__main__':
    main()