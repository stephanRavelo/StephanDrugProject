import pandas as pd
import json
import numpy as np
from typing import TextIO
from typing import Union

PATH_PROJECT = 'input/'
OUTPUT_PATH= 'output/'


def load_csv(filename: str) -> pd.DataFrame:
    """ Create a pandas dataframe based on the csv file. """

    try:
        df = pd.read_csv(filepath_or_buffer=PATH_PROJECT + filename, index_col=0)
        return df
    except IOError:
        print("Error: There is no such file or directory for CSV Files")


def load_csv_bis(filename: str) -> pd.DataFrame:
    """ Create a pandas dataframe based on the csv file. Also renaming columns knowing the different possible cases"""
    column_pattern = ["id", "title", "date", "journal"]

    try:
        df = pd.read_csv(filepath_or_buffer=PATH_PROJECT + filename, index_col=0)
        if list(df.columns) != column_pattern:
            # knowing that the clinical trial file has a different structure. Add here if there are other cases
            df.rename(columns={"scientific_title": "title"}, inplace=True)
        return df
    except IOError:
        print("Error: There is no such file or directory for CSV Files")


def load_json(filename: str) -> pd.DataFrame:
    """ Create a pandas dataframe based on the input JSON file.
    It does some formatting operations (e.g: removing carriage return, square brackets and empty space) """

    with open(PATH_PROJECT+filename, "r") as f:
        content = f.read() \
            .replace('\n', '') \
            .replace("[", '') \
            .replace(",]", '') \
            .strip()
        res = pd.read_json(content, lines=True)
    return res


def load_files(csv_files: 'list[str]', json_files: 'list[str]') -> pd.DataFrame:
    """ Load the csv and json files to return all in a pandas dataframe """
    df_list = list()  # list containing the different dataframes

    for csvFile in csv_files:
        df_csv = load_csv_bis(csvFile)
        df_list.append(df_csv)

    for jsonFile in json_files:
        df_json = load_json(jsonFile)
        df_list.append(df_json)

    df = pd.concat(df_list, sort=True).set_index('id')
    return df


def enhanced_load_files(csv_pubmed_files: 'list[str]', csv_clinical_files: 'list[str]', json_files: 'list[str]') -> pd.DataFrame:
    """ Load the pubmed csv, clinical csv and json files to return a pandas dataframe """
    df_list = list()  # list containing the different dataframes

    # csv pubmed files
    for csv_pubmed_file in csv_pubmed_files:
        df_pubmed_csv = load_csv_bis(csv_pubmed_file)
        # adding the type of source
        df_pubmed_csv["SourceFile"] = "PubMed"
        df_list.append(df_pubmed_csv)

    # csv clinical files
    for csvClinicalFile in csv_clinical_files:
        df_clinical_csv = load_csv_bis(csvClinicalFile)
        # adding the type of source
        df_clinical_csv["SourceFile"] = "ClinicalTrial"
        df_list.append(df_clinical_csv)

    for json_file in json_files:
        df_json = load_json(json_file)
        df_json["SourceFile"] = "PubMed"  # assuming that only pubmed files are received as a json
        df_list.append(df_json)

    df = pd.concat(df_list, sort=True).set_index('id')
    return df


def formatting_date(df: pd.DataFrame) -> pd.DataFrame:
    """ Format the date column in order to have a common date pattern. """
    df['date'] = pd.to_datetime(df['date'])  # homogenous date structure
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')  # stringify dates
    return df


def cleaning_df (df : pd.DataFrame) -> pd.DataFrame :
    """
    return a dataframe without blank space or NaN data
    """
    df["title"]=df["title"].str.strip() # remove empty lines
    df["title"]=df["title"].replace('', np.nan) # replace blank space to NaN
    df.dropna(axis=0,inplace=True)
    return df


def finding_mention(substring: str, df_reference: pd.DataFrame, search_col: str = "title") -> pd.DataFrame:
    """ Return a df that contains the substring in a specified dataframe of reference (e.g: pubmed dataframe).
    If no match is found, return an empty df"""


    df = pd.DataFrame(columns=['title', 'journal', 'date'])
    df = df_reference[df_reference[search_col].str.contains(substring, case=False)]
    return df


def finding_pubmed_mention(substring: str, df_reference: pd.DataFrame, search_col: str = "title") -> pd.DataFrame:
    """ Return a df that contains the substring in a specified dataframe of reference (e.g: pubmed dataframe).
    If no match is found, return an empty df"""

    df = pd.DataFrame(columns=['title', 'journal', 'date'])
    df_reference = df_reference.loc[df_reference["SourceFile"] == "PubMed"]
    df = df_reference[df_reference[search_col].str.contains(substring, case=False)]
    return df


def finding_clinical_mention(substring: str, df_reference: pd.DataFrame, search_col: str = "title") -> pd.DataFrame:
    """ Return a df that contains the substring in a specified dataframe of reference (e.g: pubmed dataframe).
    If no match is found, return an empty df"""

    df = pd.DataFrame(columns=['title', 'journal', 'date'])
    df_reference = df_reference.loc[df_reference["SourceFile"] == "ClinicalTrial"]
    df = df_reference[df_reference[search_col].str.contains(substring, case=False)]
    return df


def generate_link(df_drugs: pd.DataFrame, df_reference: pd.DataFrame) -> {}:
    """ return a python dict including the link graph between the drugs and the different publication in the journal
    and scientific trials"""

    drug_dict = dict()
    # define a list of drugs. Faster to loop on a list than on a pandas df.
    drugs = df_drugs['drug'].to_list()
    # print("drugs" ,+ drugs )

    for drug in drugs:
        drug_dict[drug] = dict()

        # pubMed
        drug_dict[drug]["pubMed"] = finding_mention(drug, df_reference, "title")["title"].to_list()
        drug_dict[drug]["pubMedJournal"] = finding_mention(drug, df_reference, "title")["journal"].to_list()
        drug_dict[drug]["pubMedDate"] = finding_mention(drug, df_reference, "title")["date"].to_list()

        # clinical_trials
        drug_dict[drug]["clinicalTrial"] = finding_mention(drug, df_reference, "title")["title"].to_list()
        drug_dict[drug]["clinicalTrialJournal"] = finding_mention(drug, df_reference, "title")["journal"].to_list()
        drug_dict[drug]["clinicalTrialDate"] = finding_mention(drug, df_reference, "title")["date"].to_list()
    return drug_dict


def enhanced_generate_link(df_drugs: pd.DataFrame, df_reference: pd.DataFrame) -> {}:
    """ return a python dict including the link graph between the drugs and the different publication in the journal
    and scientific trials"""

    drug_dict = dict()
    # define a list of drugs. Faster to loop on a list than on a pandas df.
    drugs = df_drugs['drug'].to_list()

    for drug in drugs:
        drug_dict[drug] = dict()

        # pubMed
        drug_dict[drug]["pubMed"] = finding_pubmed_mention(drug, df_reference, "title")["title"].to_list()
        drug_dict[drug]["pubMedJournal"] = finding_pubmed_mention(drug, df_reference, "title")["journal"].to_list()
        drug_dict[drug]["pubMedDate"] = finding_pubmed_mention(drug, df_reference, "title")["date"].to_list()

        # clinical_trials
        drug_dict[drug]["clinicalTrial"] = finding_clinical_mention(drug, df_reference, "title")["title"].to_list()
        drug_dict[drug]["clinicalTrialJournal"] = finding_clinical_mention(drug, df_reference, "title")[
            "journal"].to_list()
        drug_dict[drug]["clinicalTrialDate"] = finding_clinical_mention(drug, df_reference, "title")["date"].to_list()
    return drug_dict


def enhanced_generate_link_list(df_drugs: pd.DataFrame, df_reference: pd.DataFrame) -> 'list({})':
    """ return a list of python dictionnaries (inspired by the pubmed.json file) including the link graph between the drugs and the different publication in the journal
    and scientific trials"""

    drug_dict = dict()
    res = list()
    # define a list of drugs. Faster to loop on a list than on a pandas df.
    drugs = df_drugs['drug'].to_list()

    for drug in (drugs):
        drug_dict["drugName"] = drug

        # PubMed
        drug_dict["pubMed"] = finding_pubmed_mention(drug, df_reference, "title")["title"].to_list()
        drug_dict["pubMedJournal"] = finding_pubmed_mention(drug, df_reference, "title")["journal"].to_list()
        drug_dict["pubMedDate"] = finding_pubmed_mention(drug, df_reference, "title")["date"].to_list()

        # Clinical_trials
        drug_dict["clinicalTrial"] = finding_clinical_mention(drug, df_reference, "title")["title"].to_list()
        drug_dict["clinicalTrialJournal"] = finding_clinical_mention(drug, df_reference, "title")["journal"].to_list()
        drug_dict["clinicalTrialDate"] = finding_clinical_mention(drug, df_reference, "title")["date"].to_list()
        res.append(dict(drug_dict.items()))
    return res


def generate_json_file(filepath: str, drug_link: any) -> any:
    """ Generate the json file representing the link between drugs and the different pubmed and clinical trials"""
    try :
        with open(OUTPUT_PATH + 'generatedDrugLink.json', 'a') as fp:
            #Open file in append mode. If file does not exist, it creates a new file.
            json.dump(drug_link, fp, indent=2, sort_keys=False)
    except IOError:
        print("Error: Please verify the input ")