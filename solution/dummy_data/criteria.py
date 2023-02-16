recommendation_criteria_dict = {
    "compare_keys": [
        {
            "key": "primary_cuisine",
            "desc": "Sets the primary cuisine of the user -> List of primary cuisines",
            "type": "array",
            "attribute_type": "user_property",
            "array": {
                "array_key": "cuisines",
                "start_index": 0,
                "end_index": 1,
                "extract_key": "type",
                "sort": {
                    "key": "noOfOrders",
                    "order": "desc"
                }
            },

        },
        {
            "key": "secondary_cuisine",
            "desc": "Sets the secondary cuisine of the user -> List of secondary cuisines",
            "type": "array",
            "attribute_type": "user_property",
            "array": {
                "array_key": "cuisines",
                "start_index": 1,
                "end_index": 3,
                "extract_key": "type",
                "sort": {
                    "key": "noOfOrders",
                    "order": "desc"
                }
            },
        },
        {
            "key": "primary_cost_bracket",
            "desc": "Sets the primary cost_bracket of the user -> List of primary cost_bracket",
            "type": "array",
            "attribute_type": "user_property",
            "array": {
                "array_key": "costBracket",
                "start_index": 0,
                "end_index": 1,
                "extract_key": "type",
                "convert_into_integer": True,
                "sort": {
                    "key": "noOfOrders",
                    "order": "desc"
                }
            },

        },
        {
            "key": "secondary_cost_bracket",
            "desc": "Sets the secondary cost_bracket of the user -> List of secondary cost_bracket",
            "type": "array",
            "attribute_type": "user_property",
            "array": {
                "array_key": "costBracket",
                "start_index": 1,
                "end_index": 3,
                "extract_key": "type",
                "convert_into_integer": True,
                "sort": {
                    "key": "noOfOrders",
                    "order": "desc"
                }
            },
        },
        {
            "key": "newly_created_restaurants",
            "desc": "Sets the list of new restaurants",
            "type": "array",
            "attribute_type": "restaurants",
            "array": {
                "array_key": "costBracket",
                "start_index": 0,
                "end_index": 4,
                "extract_key": "restaurantId",
                "convert_into_integer": True,
                "filter": {
                    "key": "onboardedTime",
                    "operator": "GTE",
                    "value": 48,
                    "unit": "time_before",
                    "time_unit": "hours"
                },
                "sort": {
                    "key": "rating",
                    "order": "desc"
                }
            },
        }
    ],
    "conditions": [
        {
            "criteria": [
                {
                    "key": "isRecommended",
                    "type": "SIMPLE_COMPARE",
                    "value": True,
                    "operation": "EQ"
                },
                {
                    "key": "cuisine",
                    "attr_key": "primary_cuisine",
                    "type": "ATTR_COMPARE",
                    "operation": "IN"
                },
                {
                    "key": "costBracket",
                    "attr_key": "primary_cost_bracket",
                    "type": "ATTR_COMPARE",
                    "operation": "IN"
                }
            ],
            "combination_type": "AND",
            "fallback": [
                {
                    "criteria": [
                        {
                            "key": "isRecommended",
                            "type": "SIMPLE_COMPARE",
                            "value": True,
                            "operation": "EQ"
                        },
                        {
                            "key": "cuisine",
                            "attr_key": "primary_cuisine",
                            "type": "ATTR_COMPARE",
                            "operation": "IN"
                        },
                        {
                            "key": "costBracket",
                            "attr_key": "secondary_cost_bracket",
                            "type": "ATTR_COMPARE",
                            "operation": "IN"
                        }
                    ],
                    "combination_type": "AND",
                },
                {
                    "criteria": [
                        {
                            "key": "isRecommended",
                            "type": "SIMPLE_COMPARE",
                            "value": True,
                            "operation": "EQ"
                        },
                        {
                            "key": "cuisine",
                            "attr_key": "secondary_cuisine",
                            "type": "ATTR_COMPARE",
                            "operation": "IN"
                        },
                        {
                            "key": "costBracket",
                            "attr_key": "primary_cost_bracket",
                            "type": "ATTR_COMPARE",
                            "operation": "IN"
                        }
                    ],
                    "combination_type": "AND",
                }
            ]
        },
        {
            "criteria": [
                {
                    "key": "cuisine",
                    "attr_key": "primary_cuisine",
                    "type": "ATTR_COMPARE",
                    "operation": "IN"
                },
                {
                    "key": "costBracket",
                    "attr_key": "primary_cost_bracket",
                    "type": "ATTR_COMPARE",
                    "operation": "IN"
                },
                {
                    "key": "rating",
                    "type": "SIMPLE_COMPARE",
                    "value": 4,
                    "operation": "GTE"
                }
            ],
            "combination_type": "AND"
        },
        {
            "criteria": [
                {
                    "key": "cuisine",
                    "attr_key": "primary_cuisine",
                    "type": "ATTR_COMPARE",
                    "operation": "IN"
                },
                {
                    "key": "costBracket",
                    "attr_key": "secondary_cost_bracket",
                    "type": "ATTR_COMPARE",
                    "operation": "IN"
                },
                {
                    "key": "rating",
                    "type": "SIMPLE_COMPARE",
                    "value": 4.5,
                    "operation": "GTE"
                }
            ],
            "combination_type": "AND"
        },
        {
            "criteria": [
                {
                    "key": "cuisine",
                    "attr_key": "secondary_cuisine",
                    "type": "ATTR_COMPARE",
                    "operation": "IN"
                },
                {
                    "key": "costBracket",
                    "attr_key": "primary_cost_bracket",
                    "type": "ATTR_COMPARE",
                    "operation": "IN"
                },
                {
                    "key": "rating",
                    "type": "SIMPLE_COMPARE",
                    "value": 4.5,
                    "operation": "GTE"
                }
            ],
            "combination_type": "AND"
        },
        {
            "criteria": [
                {
                    "key": "restaurantId",
                    "attr_key": "newly_created_restaurants",
                    "type": "ATTR_COMPARE",
                    "operation": "IN"
                }
            ],
            "combination_type": "AND"
        },
        {
            "criteria": [
                {
                    "key": "cuisine",
                    "attr_key": "primary_cuisine",
                    "type": "ATTR_COMPARE",
                    "operation": "IN"
                },
                {
                    "key": "costBracket",
                    "attr_key": "primary_cost_bracket",
                    "type": "ATTR_COMPARE",
                    "operation": "IN"
                },
                {
                    "key": "rating",
                    "type": "SIMPLE_COMPARE",
                    "value": 4,
                    "operation": "LT"
                }
            ],
            "combination_type": "AND"
        },
        {
            "criteria": [
                {
                    "key": "cuisine",
                    "attr_key": "primary_cuisine",
                    "type": "ATTR_COMPARE",
                    "operation": "IN"
                },
                {
                    "key": "costBracket",
                    "attr_key": "secondary_cost_bracket",
                    "type": "ATTR_COMPARE",
                    "operation": "IN"
                },
                {
                    "key": "rating",
                    "type": "SIMPLE_COMPARE",
                    "value": 4.5,
                    "operation": "LT"
                }
            ],
            "combination_type": "AND"
        },
        {
            "criteria": [
                {
                    "key": "cuisine",
                    "attr_key": "secondary_cuisine",
                    "type": "ATTR_COMPARE",
                    "operation": "IN"
                },
                {
                    "key": "costBracket",
                    "attr_key": "primary_cost_bracket",
                    "type": "ATTR_COMPARE",
                    "operation": "IN"
                },
                {
                    "key": "rating",
                    "type": "SIMPLE_COMPARE",
                    "value": 4.5,
                    "operation": "LT"
                }
            ],
            "combination_type": "AND"
        },
        {
            "criteria": [],
            "combination_type": "AND"
        }
    ]
}
