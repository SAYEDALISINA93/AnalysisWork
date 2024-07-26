import ast
import os

import pandas as pd


def serialize_map(string):
    try:
        data_dict = ast.literal_eval(string)
        # Convert keys to numbers
        try:
            data_dict = {int(key) if key.isdigit() else key: value for key, value in data_dict.items()}
            return data_dict
        except Exception:
            return {}
    except Exception:
        return {}


def serialize(string):
    try:
        return ast.literal_eval(string)
    except Exception:
        return []


def serialize_question_choices(questions_df):
    questions_df['choices'] = questions_df['choices'].apply(lambda x: serialize_map(x))
    questions_df['choices'] = questions_df.apply(lambda row: {**row['choices'], int(0): row['not_applicable_choice']},
                                                 axis=1)
    return questions_df


def load_user_data(path):
    loaded_data = {}
    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)
        if os.path.isfile(file_path):
            try:
                loaded_data[file_name.split('.')[0]] = pd.read_csv(file_path, encoding='utf-8')
            except Exception:
                pass
    return loaded_data


def minimize_recipes(recipes_df, valid_recipe_ids):
    recipes_df = recipes_df[recipes_df['new_recipe_id'].isin(valid_recipe_ids['recipe_id'])]
    recipes_df = recipes_df.reset_index(drop=True)

    return recipes_df
