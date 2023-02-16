from .dummy_data.criteria import recommendation_criteria_dict
from .dto import User, RecCriteriaUserKeyType, RecCriteria, RecCriteriaUserKey, RecCriteriaUserKeySortType, Restaurant, \
    RecCriteriaUserKeyAttrType, RecCriteriaUserKeyArrayFilter, RecCriteriaUserKeyOperator, \
    RecCriteriaUserKeyArrayFilterUnitType
from typing import List
from datetime import datetime
from datetime import timedelta


class ComparePropertyGenerator:
    def __init__(self, user: User, available_restaurants: List[Restaurant]):
        """
        just neatly forms a usable dictionary
        {'primary_cuisine': ['Chinese'], 'secondary_cuisine': ['SouthIndian', 'NorthIndian'], 'primary_cost_bracket': [5], 'secondary_cost_bracket': [4, 3], 'newly_created_restaurants': [3, 4, 5]}
        :param user:
        :param available_restaurants:
        """
        self.recommendation_criteria = RecCriteria(**recommendation_criteria_dict)
        self.user = user
        self.available_restaurants = available_restaurants
        self.sorted_map = {}

    def _getArrayValue(self, criteria_filter: RecCriteriaUserKeyArrayFilter):
        value = None
        if criteria_filter.unit == RecCriteriaUserKeyArrayFilterUnitType.time_before:
            d = {criteria_filter.time_unit: criteria_filter.value}
            value = datetime.utcnow().date() - timedelta(**d)
        return value

    def _filterArray(self, criteria_filter: RecCriteriaUserKeyArrayFilter):
        def criteria_matcher(elem):
            value = getattr(elem, criteria_filter.key)
            if criteria_filter.operator == RecCriteriaUserKeyOperator.GTE:
                return value >= self._getArrayValue(criteria_filter)

        return criteria_matcher

    def _extractArray(self, criteria: RecCriteriaUserKey):
        start_index = criteria.array.start_index
        end_index = criteria.array.end_index
        extract_key = criteria.array.extract_key
        sort_key = criteria.array.sort.key
        sort_order = criteria.array.sort.order
        user_array_key = criteria.array.array_key
        attribute_type = criteria.attribute_type
        criteria_filter = criteria.array.filter
        sorted_array = []

        # This is to uniquely define a key, so sorting doesn't repeat
        sorted_key = f"{criteria.attribute_type}::{sort_key}::{sort_order}"

        # two types of array to extract data from -> user and restaurants (new restaurants)
        if attribute_type == RecCriteriaUserKeyAttrType.user_property:
            sorted_key = f"{criteria.attribute_type}::{user_array_key}::{sort_key}::{sort_order}"
            sorted_array = getattr(self.user, user_array_key)

        if attribute_type == RecCriteriaUserKeyAttrType.restaurants:
            sorted_key = f"{criteria.attribute_type}::{sort_key}::{sort_order}"
            sorted_array = self.available_restaurants

        if criteria_filter:
            sorted_array = list(filter(self._filterArray(criteria_filter), sorted_array))

        if sorted_key in self.sorted_map:
            sorted_array = self.sorted_map.get(sorted_key)
        else:
            sorted_array = sorted(sorted_array, key=lambda x: getattr(x, sort_key),
                                  reverse=sort_order == RecCriteriaUserKeySortType.desc)
            self.sorted_map.update({sorted_key: sorted_array})

        result = [getattr(x, extract_key) for x in sorted_array[start_index:end_index]]
        if criteria.array.convert_into_integer:
            result = [int(x) for x in result]
        return result

    def get_properties(self):
        """
        just neatly forms a usable dictionary
        {'primary_cuisine': ['Chinese'], 'secondary_cuisine': ['SouthIndian', 'NorthIndian'], 'primary_cost_bracket': [5], 'secondary_cost_bracket': [4, 3], 'newly_created_restaurants': [3, 4, 5]}
        :param user:
        :param available_restaurants:
        """
        user_properties = {}
        for criteria in self.recommendation_criteria.compare_keys:
            if criteria.type == RecCriteriaUserKeyType.array:
                value = self._extractArray(criteria=criteria)
                user_properties.update({criteria.key: value})
        return user_properties
