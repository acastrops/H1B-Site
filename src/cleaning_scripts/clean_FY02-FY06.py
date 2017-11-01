import numpy as np
import pandas as pd

df = pd.read_csv('../../../data/clean/H1B_FY02-FY06.csv', encoding='latin1', sep='~',
                 usecols=["CASE_NO", "NAME", "CITY", "STATE",
                          "POSTAL_CODE", "NBR_IMMIGRANTS", "JOB_CODE",
                          "BEGIN_DATE", "END_DATE", "WAGE_RATE_1",
                          "RATE_PER_1", "PREVAILING_WAGE_1"],
                 dtype={"CASE_NO": str, "NAME": str, "CITY": str,
                        "STATE": str, "POSTAL_CODE": str,
                        "JOB_CODE": str, "RATE_PER_1": str,
                        "NBR_IMMIGRANTS": np.float64,
                        "BEGIN_DATE": str})

# Convert nbr_immigrants to integer, there's no NaN value for ints so
# have to give it an impossible value of -1
df['NBR_IMMIGRANTS'] = df.NBR_IMMIGRANTS.apply(lambda x: -1 if np.isnan(x) else np.int32(x))

# Add leading zeros to job_code to match codes in job_codes.csv
df['JOB_CODE'] = df.JOB_CODE.apply(lambda x: '0'*(3-len(str(x))) + x)

employers = df[["NAME", "CITY", "STATE", "POSTAL_CODE"]].drop_duplicates()

employers = employers.rename(columns={
    "NAME": "Name",
    "CITY": "City",
    "STATE": "State",
    "POSTAL_CODE": "Postal_Code"})

employers = employers.reset_index().rename(columns={'index': 'id_'})

# Allows cases to have associated employer_id
df = df.set_index("NAME").join(employers.set_index("Name"), how="outer")


# Set up cases format
cases = df[["NBR_IMMIGRANTS", "JOB_CODE", "id_", "BEGIN_DATE", "END_DATE",
            "WAGE_RATE_1", "RATE_PER_1", "PREVAILING_WAGE_1"]]
cases.reset_index(drop=True, inplace=True)
cases.reset_index(inplace=True)

cases = cases.rename(columns={
    "index": "id_",
    "NBR_IMMIGRANTS": "Nbr_Immigrants",
    "JOB_CODE": "Job_Code",
    "BEGIN_DATE": "Begin_Date",
    "END_DATE": "End_Date",
    "WAGE_RATE_1": "Wage_Rate",
    "RATE_PER_1": "Rate_Per",
    "PREVAILING_WAGE_1": "Prevailing_Wage",
    "id_": "Employer_Id"
})

# Write files
employers.to_csv('../../../data/clean/employers_FY02-FY06.csv', sep='~', index=False)
cases.to_csv('../../../data/clean/cases_FY02-FY06.csv', sep='~', index=False)
