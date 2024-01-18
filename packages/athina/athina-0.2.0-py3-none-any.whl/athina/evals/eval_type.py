from enum import Enum


class LlmEvalTypeId(Enum):
    CONTEXT_CONTAINS_ENOUGH_INFORMATION = "Ccei"
    DOES_RESPONSE_ANSWER_QUERY = "Draq"
    FAITHFULNESS = "Irftc"
    GRADING_CRITERIA = "GradingCriteria"
    CUSTOM_PROMPT = "CustomPrompt"
    SUMMARY_ACCURACY = "SummaryAccuracy"

class RagasEvalTypeId(Enum):
    RAGAS_CONTEXT_RELEVANCY = "RagasContextRelevancy"
    RAGAS_ANSWER_RELEVANCY = "RagasAnswerRelevancy"

class FunctionEvalTypeId(Enum):
    REGEX = "Regex"
    CONTAINS_ANY = "ContainsAny"
    CONTAINS_ALL = "ContainsAll"
    CONTAINS = "Contains"
    CONTAINS_NONE = "ContainsNone"
    CONTAINS_JSON = "ContainsJson"
    CONTAINS_EMAIL = "ContainsEmail"
    IS_JSON = "IsJson"
    IS_EMAIL = "IsEmail"
    NO_INVALID_LINKS = "NoInvalidLinks"
    CONTAINS_LINK = "ContainsLink"
    CONTAINS_VALID_LINK = "ContainsValidLink"
    EQUALS = "Equals"
    STARTS_WITH = "StartsWith"
    ENDS_WITH = "EndsWith"
    LENGTH_LESS_THAN = "LengthLessThan"
    LENGTH_GREATER_THAN = "LengthGreaterThan"
    API_CALL = "ApiCall"