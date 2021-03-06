from utils import *


def drug_pipeline():
    # loading
    df_drugs = load_csv('drugs.csv')
    df_enhanced_input_file = enhanced_load_files(["pubmed.csv"], ["clinical_trials.csv"], ["pubmed.json"])

    # formatting and cleansing
    formatting_date(df_enhanced_input_file)
    cleaning_df(df_enhanced_input_file)

    # there are two choices for the format of the json File
    # 1 - generate a dictionary of link
    #dico_drug=enhanced_generate_link(df_drugs,df_enhanced_input_file)

    # 2 - generate a list of dictionaries
    dico_drug = enhanced_generate_link_list(df_drugs, df_enhanced_input_file)

    # generate the json file
    generate_json_file(OUTPUT_PATH,dico_drug)


drug_pipeline()


