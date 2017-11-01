import numpy as np
import pandas as pd

df = pd.read_csv("../../../data/clean/H1B_FY07.txt", encoding='latin1', sep="~",
                 usecols=["Employer_Name", "City", "State", "Zip_Code",
                          "Nbr_Immigrants", "Begin_Date", "End_Date",
                          "Occupation_Code", "Wage_Rate_From_1",
                          "Wage_Rate_Per_1", "Prevailing_Wage_1"],
                 dtype={"Zip_Code": str,
                        "Occupation_Code": str})

df.Wage_Rate_From_1 = df.Wage_Rate_From_1.str.split("$", expand=True)[1]
df.Prevailing_Wage_1 = df.Prevailing_Wage_1.str.split("$", expand=True)[1]

df['Occupation_Code'] = df.Occupation_Code.apply(lambda x: '0'*(3-len(str(x))) + str(x))
df['Nbr_Immigrants'] = df.Nbr_Immigrants.apply(lambda x: -1 if np.isnan(x) else np.int32(x))

employers = df[["Employer_Name", "City", "State", "Zip_Code"]].drop_duplicates()

employers = employers.rename(columns={
    "Employer_Name": "Name",
    "City": "City",
    "State": "State",
    "Zip_Code": "Postal_Code"})
employers = employers.reset_index().rename(columns={'index': 'id_'})

df = df.set_index("Employer_Name").join(employers.set_index("Name"), how="outer", rsuffix="_emp")

cases = df[["Nbr_Immigrants", "Occupation_Code", "id_", "Begin_Date", "End_Date",
            "Wage_Rate_From_1", "Wage_Rate_Per_1", "Prevailing_Wage_1"]]
cases.reset_index(drop=True, inplace=True)
cases.reset_index(inplace=True)

cases = cases.rename(columns={
    "index": "id_",
    "Occupation_Code": "Job_Code",
    "Wage_Rate_From_1": "Wage_Rate",
    "Wage_Rate_Per_1": "Rate_Per",
    "Prevailing_Wage_1": "Prevailing_Wage",
    "id_": "Employer_Id"
})

employers.to_csv('../../../data/clean/employers_FY07.csv', sep='~', index=False)
cases.to_csv('../../../data/clean/cases_FY07.csv', sep='~', index=False)
