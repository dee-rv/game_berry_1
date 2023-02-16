# This is a sample Python script.
from typing import List

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from solution import RecommendationEngine
from dto import User, Restaurant
from pydantic import parse_obj_as
from dummy_data.ref_user_data import user
from dummy_data.ref_rest_data import available_restaurants


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    rec = RecommendationEngine()
    result = rec.getRestaurantRecommendations(
        user=User(**user),
        available_restaurants=parse_obj_as(List[Restaurant], list(available_restaurants))
    )
    print('result', result)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
