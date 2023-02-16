# This is a sample Python script.
from typing import List

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from solution.recommended import RecommendationEngine
from solution.dto import User, Restaurant
from pydantic import parse_obj_as
from solution.dummy_data.ref_user_data import user
from solution.dummy_data.ref_rest_data import available_restaurants
from solution.dummy_data.criteria import recommendation_criteria_dict


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    rec = RecommendationEngine(
        recommendation_criteria_dict=recommendation_criteria_dict,
        limit=2,
        debug=True,
    )
    result = rec.getRestaurantRecommendations(
        user=User(**user),
        available_restaurants=parse_obj_as(List[Restaurant], list(available_restaurants))
    )
    print('result', result)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
