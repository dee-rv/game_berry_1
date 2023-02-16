from typing import List
from .dto import User, Restaurant, RecCriteria, RecCriteriaCondition, RecCriteriaConditionCombinationType, \
    RecCriteriaUserKeyOperator, RecCriteriaConditionCriteriaType, RecCriteriaConditionCriteria
from .dummy_data.criteria import recommendation_criteria_dict
from .compare_property_generator import ComparePropertyGenerator

"""
Order Conditions of Recommendation

C1 Featured restaurants of primary cuisine and primary cost bracket. If none, then all featured restaurants of primary cuisine, secondary cost and secondary cuisine, primary cost
C2 All restaurants of Primary cuisine, primary cost bracket with rating >= 4
C3 All restaurants of Primary cuisine, secondary cost bracket with rating >= 4.5
C4 All restaurants of secondary cuisine, primary cost bracket with rating >= 4.5
C5 Top 4 newly created restaurants by rating
C6 All restaurants of Primary cuisine, primary cost bracket with rating < 4
C7 All restaurants of Primary cuisine, secondary cost bracket with rating < 4.5
C8 All restaurants of secondary cuisine, primary cost bracket with rating < 4.5
C9 All restaurants of any cuisine, any cost bracket
"""


class RecommendationEngine:
    def __init__(self):
        """
        ASSUMPTIONS MADE
        1. cannot use database for indexing and optimization
        2. length of criteria <<< length of restaurants


        Can be extended to new user properties, maybe number of views of a particular cuisine
        Conditions and their order can be changed anytime

        Takes criteria as input -> dictionary/ JSON that defines the various order of recommendation as shown above
        this can be even db driven, to be changed by admin on the fly rather than by developer if admin wants to
        expiriment with sales numbers by changing the recommendation criteria
        additionally it can be db driven to do AB testing, by having different recommendation criteria for
        different days of the week
        A userfriendly UI can also be built to set and modify the recommendation JSON
        """
        self.recommendation_criteria = RecCriteria(**recommendation_criteria_dict)

        """
        represents the index of the first element in the array satisfying that particular condition,
        support we have 1000 restaurants, and we get a distribution like
        [
            20 x C1 (referenced above),
            10 x C2,
            15 x C3,
            10 x C3,
            ....
        ], condition_index_list will be = [0, 20, 30 (20+10), 45 (20+10+15), ... ] 
        """
        self.condition_index_list = [0] * len(self.recommendation_criteria.conditions)

        # final result -> returns list of restaurant ids
        self.recommended_restaurants = []

        """
        helper dict to assign user. other properties
        example : 
        {'primary_cuisine': ['Chinese'], 'secondary_cuisine': ['SouthIndian', 'NorthIndian'], 'primary_cost_bracket': [5], 'secondary_cost_bracket': [4, 3], 'newly_created_restaurants': [3, 4, 5]}
        """
        self.properties = {}

    def _isCriteriaMatching(self, restaurant: Restaurant, criteria: RecCriteriaConditionCriteria) -> bool:
        """
        function to check if particular criteria is matching a particular restaurant
        whether
        {
            "restaurantId": "1",
            "cuisine": "SouthIndian",
            "costBracket": 3,
            "rating": 1.5,
            "isRecommended": True,
            "onboardedTime": "2023-02-01",
        } matches
        {
            "key": "cuisine",
            "attr_key": "primary_cuisine",
            "type": "ATTR_COMPARE",
            "operation": "IN"
        }
        this checks if the restaurant is under primary cuisine or not
        :param restaurant:
        :param criteria:
        :return:
        """
        is_criteria_matching = True
        value = getattr(restaurant, criteria.key)
        if 'enum' in str(type(value)):
            value = getattr(value, 'value')

        """
        SIMPLE_COMPARE example -> rating > 4
        ATTR_COMPARE example -> restaurant_cuisine IN ['Chinese']
        """
        value_to_compare = None

        if criteria.type == RecCriteriaConditionCriteriaType.SIMPLE_COMPARE:
            value_to_compare = criteria.value
        if criteria.type == RecCriteriaConditionCriteriaType.ATTR_COMPARE:
            value_to_compare = self.properties.get(criteria.attr_key)

        if criteria.operation == RecCriteriaUserKeyOperator.GTE:
            is_criteria_matching = value >= value_to_compare
        if criteria.operation == RecCriteriaUserKeyOperator.IN:
            is_criteria_matching = value in value_to_compare
        if criteria.operation == RecCriteriaUserKeyOperator.LT:
            is_criteria_matching = value < value_to_compare
        if criteria.operation == RecCriteriaUserKeyOperator.EQ:
            is_criteria_matching = (value == value_to_compare)

        return is_criteria_matching

    def _isConditionMatching(self, restaurant: Restaurant, condition: RecCriteriaCondition) -> bool:
        """
        function that checks if all the criterias are matched for a given condition
        example :
        Condition : C2 All restaurants of Primary cuisine, primary cost bracket with rating >= 4
        this condition is split into 3 criteria following an AND condition
        :param restaurant:
        :param condition:
        :return:
        """
        is_condition_matching = True
        if condition.combination_type == RecCriteriaConditionCombinationType.AND:
            # all conditions must be satisfied
            for criteria in condition.criteria:
                is_criteria_matching = self._isCriteriaMatching(restaurant=restaurant, criteria=criteria)
                if not is_criteria_matching:
                    is_condition_matching = False
                    break
        return is_condition_matching

    def _getMatchingCondition(self, restaurant: Restaurant) -> int:
        """
        function that returns which condition matched, C1, C2, .... C9 -> returns index of array 0, 1 ... 8
        :param restaurant:
        :return:
        """
        for index in range(len(self.recommendation_criteria.conditions)):
            condition = self.recommendation_criteria.conditions[index]
            is_matching = self._isConditionMatching(restaurant=restaurant, condition=condition)
            if is_matching:
                return index
            if condition.fallback:
                for fallback_condition in condition.fallback:
                    is_matching = self._isConditionMatching(restaurant=restaurant, condition=fallback_condition)
                    if is_matching:
                        return index

    def _setConditionArray(self, condition_number: int):
        """
        function to just increment condition_index_list
        :param condition_number:
        :return:
        """
        for index in range(condition_number + 1, len(self.condition_index_list)):
            self.condition_index_list[index] += 1

    def _sortViaConditions(self, available_restaurants: List[Restaurant]):
        for restaurant in available_restaurants:
            condition_number = self._getMatchingCondition(restaurant=restaurant)
            if condition_number is not None:
                # self.condition_index_list[condition_number]
                # as improvement, random index int can be generated to not show the same order to the user
                # index = random.randint(self.condition_index_list[condition_number], self.condition_index_list[condition_number+1] if condition_number < len(self.condition_index_list) -1 else len(self.condition_index_list))
                index = self.condition_index_list[condition_number]
                self._setConditionArray(condition_number)

                # inserts the restaurant into the appropriate order based on condition number satisfied
                self.recommended_restaurants.insert(index, str(restaurant.restaurantId))

    def getRestaurantRecommendations(self, user: User, available_restaurants: List[Restaurant]) -> List[str]:
        """
        main function that returns list of rest ids
        :param user:
        :param available_restaurants:
        :return:
        """
        upg = ComparePropertyGenerator(user=user, available_restaurants=available_restaurants)
        """
        user and other properties are updated
        {'primary_cuisine': ['Chinese'], 'secondary_cuisine': ['SouthIndian', 'NorthIndian'], 'primary_cost_bracket': [5], 'secondary_cost_bracket': [4, 3], 'newly_created_restaurants': [3, 4, 5]}
        """
        properties = upg.get_properties()

        self.properties.update(properties)

        # main sorting function
        self._sortViaConditions(
            available_restaurants=available_restaurants
        )
        return self.recommended_restaurants
