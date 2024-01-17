from enum import Enum


class TaskType(str, Enum):
    """Enum for task types"""

    CLASSIFICATION = "classification"
    MULTILABEL_CLASSIFICATION = "multilabel_classification"
    ATTRIBUTE_EXTRACTION = "attribute_extraction"
