from enum import Enum
from typing import Optional, List, Any, Union
from typing import ForwardRef

from pydantic import BaseModel


class RecCriteriaUserKeyType(str, Enum):
    array = 'array'


class RecCriteriaUserKeySortType(str, Enum):
    desc = 'desc'
    asc = 'asc'


class RecCriteriaUserKeyAttrType(str, Enum):
    user_property = 'user_property'
    restaurants = 'restaurants'


class RecCriteriaUserKeyOperator(str, Enum):
    GTE = 'GTE'
    IN = 'IN'
    LT = 'LT'
    EQ = 'EQ'


class RecCriteriaUserKeyArrayFilterUnitType(str, Enum):
    time_before = 'time_before'


class RecCriteriaUserKeyArrayFilterTimeUnit(str, Enum):
    hours = 'hours'


class RecCriteriaUserKeySort(BaseModel):
    key: str
    order: RecCriteriaUserKeySortType


class RecCriteriaUserKeyArrayFilter(BaseModel):
    key: str
    operator: RecCriteriaUserKeyOperator
    value: float
    unit: RecCriteriaUserKeyArrayFilterUnitType
    time_unit: Optional[RecCriteriaUserKeyArrayFilterTimeUnit]


class RecCriteriaUserKeyArray(BaseModel):
    start_index: int
    end_index: int
    array_key: str
    extract_key: str
    convert_into_integer: Optional[bool]
    sort: RecCriteriaUserKeySort
    filter: Optional[RecCriteriaUserKeyArrayFilter]


class RecCriteriaUserKey(BaseModel):
    key: str
    attribute_type: RecCriteriaUserKeyAttrType
    type: RecCriteriaUserKeyType
    array: Optional[RecCriteriaUserKeyArray]


class RecCriteriaConditionCriteriaType(str, Enum):
    ATTR_COMPARE = 'ATTR_COMPARE'
    SIMPLE_COMPARE = 'SIMPLE_COMPARE'


class RecCriteriaConditionCriteria(BaseModel):
    key: str
    attr_key: Optional[str]
    type: RecCriteriaConditionCriteriaType
    operation: RecCriteriaUserKeyOperator
    value: Optional[Any]


class RecCriteriaConditionCombinationType(str, Enum):
    AND = 'AND'


RecCriteriaConditionRef = ForwardRef("RecCriteriaCondition")


class RecCriteriaCondition(BaseModel):
    criteria: List[RecCriteriaConditionCriteria]
    combination_type: RecCriteriaConditionCombinationType
    fallback: Optional[List[RecCriteriaConditionRef]]


class RecCriteria(BaseModel):
    """
    set of keys with which the engine compares to filter the condition
    example : primary_cuisine, property derived from user attributes
    """
    compare_keys: List[RecCriteriaUserKey]
    """
    Configuration set to order the engine
    
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
    conditions: List[RecCriteriaCondition]
