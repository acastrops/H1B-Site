import numpy as np
import pandas as pd

df = []

print('Starting cleaning...')
# Read in each file and concat them together
for i in range(6, 18):

    if i == 6:
        filename = 'FY02-FY06'
    elif i < 10:
        filename = 'FY0{}'.format(i)
    else:
        filename = 'FY{}'.format(i)

    if i == 7:
        usecols = ["Employer_Name", "City", "State",
                   "Zip_Code", "Nbr_Immigrants", "Job_Title",
                   "Begin_Date", "End_Date", "Wage_Rate_From_1",
                   "Wage_Rate_Per_1", "Prevailing_Wage_1", "Program_Designation"]
    elif i in [6, 8]:
        usecols = ["NAME", "CITY", "STATE",
                   "POSTAL_CODE", "NBR_IMMIGRANTS", "JOB_TITLE",
                   "BEGIN_DATE", "END_DATE", "WAGE_RATE_1",
                   "RATE_PER_1", "PREVAILING_WAGE_1"]
    elif i == 9 or i in range(11, 15):
        usecols = ["LCA_CASE_EMPLOYER_NAME", "LCA_CASE_EMPLOYER_CITY", "LCA_CASE_EMPLOYER_STATE",
                   "LCA_CASE_EMPLOYER_POSTAL_CODE", "TOTAL_WORKERS", "LCA_CASE_JOB_TITLE",
                   "LCA_CASE_EMPLOYMENT_START_DATE", "LCA_CASE_EMPLOYMENT_END_DATE", "LCA_CASE_WAGE_RATE_FROM",
                   "LCA_CASE_WAGE_RATE_UNIT", "PW_1", "VISA_CLASS"]
    elif i == 10:
        usecols = ["LCA_CASE_EMPLOYER_NAME", "LCA_CASE_EMPLOYER_CITY", "LCA_CASE_EMPLOYER_STATE",
                   "LCA_CASE_EMPLOYER_POSTAL_CODE", "TOTAL_WORKERS", "LCA_CASE_JOB_TITLE",
                   "LCA_CASE_EMPLOYMENT_START_DATE", "LCA_CASE_EMPLOYMENT_END_DATE", "LCA_CASE_WAGE_RATE_FROM",
                   "PW_UNIT_1", "PW_1"]
    elif i == 15:
        usecols = ["EMPLOYER_NAME", "EMPLOYER_CITY", "EMPLOYER_STATE",
                   "EMPLOYER_POSTAL_CODE", "TOTAL_WORKERS", "JOB_TITLE",
                   "EMPLOYMENT_START_DATE", "EMPLOYMENT_END_DATE", "WAGE_RATE_OF_PAY",
                   "WAGE_UNIT_OF_PAY", "PREVAILING_WAGE", "VISA_CLASS"]
    else:
        usecols = ["EMPLOYER_NAME", "EMPLOYER_CITY", "EMPLOYER_STATE",
                   "EMPLOYER_POSTAL_CODE", "TOTAL_WORKERS", "JOB_TITLE",
                   "EMPLOYMENT_START_DATE", "EMPLOYMENT_END_DATE", "WAGE_RATE_OF_PAY_FROM",
                   "WAGE_UNIT_OF_PAY", "PREVAILING_WAGE", "VISA_CLASS"]

    filename = '../data/clean/H1B_{}.csv'.format(filename)

    names = ["Name", "City", "State",
             "Postal_Code", "Nbr_Immigrants", "Job_Title",
             "Begin_Date", "End_Date", "Wage_Rate",
             "Rate_Per", "Prevailing_Wage", "Visa_Class"]
    if i not in [6, 8, 10]:
        names.append('Visa_Class')

    df.append(pd.read_csv(filename, sep='~',
                          usecols=usecols,
                          dtype={usecols[3]: str},
                          encoding='latin1',
                          low_memory=False))

    df[-1] = df[-1].rename(columns=dict(zip(usecols, names)))
    df[-1]['Name'] = df[-1].Name.str.replace('_', ' ')
    df[-1]['City'] = df[-1].City.str.replace('_', ' ')
    df[-1]['Job_Title'] = df[-1].Job_Title.str.replace('_', ' ')
    if i not in [6, 8, 10]:
        df[-1] = df[-1][df[-1].Visa_Class == 'R']

    print("Loaded {}".format(filename))

# Concat the individual years
df = pd.concat(df)

print('Loaded!\nProcessing...')

# We don't need this column anymore
df = df.drop('Visa_Class', axis=1)

# Removes the float
df['Nbr_Immigrants'] = df.Nbr_Immigrants.apply(lambda x: -1 if np.isnan(x) else np.int32(x))

# Creates a dataframe of unique employers and assigns each a code
employers = df[["Name", "City", "State", "Postal_Code"]].drop_duplicates()
employers = employers.reset_index().rename(columns={'index': 'id'})

print('Joining...')
# Joins df on the employers to assign and employer_id to each case
df = df.set_index("Name").join(employers.set_index("Name"), how="outer", rsuffix="_emp")

# Creates the cases dataframe
cases = df[["Nbr_Immigrants", "Job_Title", "id", "Begin_Date", "End_Date",
            "Wage_Rate", "Rate_Per", "Prevailing_Wage"]]

cases.reset_index(drop=True, inplace=True)
cases.reset_index(inplace=True)

cases = cases.rename(columns={
    "index": "id",
    "id": "Employer_Id"
})

print('Writing...')
# Writes the files
employers.to_csv('../data/clean/employers_all.csv', sep='~', index=False)
cases.to_csv('../data/clean/cases_all.csv', sep='~', index=False)
print('All done!')
