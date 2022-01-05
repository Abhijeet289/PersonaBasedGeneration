import pandas as pd
import json

def read_data():
    google_sheet_id = "1Osl3p1MVKL7NAF3TAr4V3EoUmn-GTTUXTz1yP8vF99E"
    sheet_name = "CombinedSheet"
    google_sheet_url = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(google_sheet_id, sheet_name)
    df = pd.read_csv(google_sheet_url)
    return df

def main():
    # Reading the data from Google Sheet
    df = read_data()

    with open('data/train_dials.json') as f:
        train_dials = json.load(f)

    with open('data/val_dials.json') as f:
        val_dials = json.load(f)

    # These are the labels for personalities
    '''
    Name	        Label
    Credibility	      1
    Emotional         2
    Logical	          3
    Personal          4
    Persona based     5
    Default	          0
    '''

    dialogue_number = 1
    persuasion_id = 0
    for i in df.index:
        curr_dialogue_number = df['USER'][i]
        if str(dialogue_number) == curr_dialogue_number:
            if dialogue_number != 1:
                if str(dialogue_number-1) in train_dials:
                    train_dials[str(dialogue_number-1)]["personality"] = persuasion_id
                    # print("dialogue {} present in train dials".format(dialogue_number-1))
                if str(dialogue_number-1) in val_dials:
                    val_dials[str(dialogue_number-1)]["personality"] = persuasion_id
                    # print("dialogue {} present in val dials".format(dialogue_number-1))
            # print("dialogue_number : ", dialogue_number)
            dialogue_number += 1
        else:
            if df['Persuasion Strategy'][i] != df['Persuasion Strategy'][i]:
                continue
            persuasion_id = int(df['Persuasion Strategy'][i])
    # print(df['Persuasion Strategy'][i])
    with open('data/train_dials.json', 'w') as f:
        json.dump(train_dials, f, indent=4)
    with open('data/val_dials.json', 'w') as f:
        json.dump(val_dials, f, indent=4)

if __name__ == "__main__":
    main()

