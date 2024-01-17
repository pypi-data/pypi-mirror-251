from dataclasses import dataclass, field
from enum import Enum
from typing import Literal

from merlin_ai import ai_model, ai_enum_model
from merlin_ai.ai_classes import OpenAIModel, OpenAIEnumModel


#@ai_enum_model(model="gpt-4-1106-preview")
class Color(Enum):
    """Most beautiful color in the world"""
    RED = 1, "the color red"
    GREEN = 2, "the color green"
    BLUE = 3, "the color blue"


@dataclass
class Record:
    category: Color
    explanation: str


# @ai_model(model="gpt-4-1106-preview")
@dataclass
class ParsedDeal:
    """
    A representation of the sales deal in the sales pipeline. The deal can be very early stage (lead, target contact identified), or very late stage, or even already a customer. It can be open or already closed (won or lost).
    """

    prospect_domain: str = field(
        metadata={
            "description": "A single most probable domain of the prospect(s), as chosen from the list of possible prospect domains."
        }
    )
    prospect_contacts: list[str] = field(
        metadata={
            "description": "Email addresses of prospect contacts, who are somehow related to the deal"
        }
    )
    excitement_level: Literal[
        "UNDETERMINED", "LOW", "LOW-TO-MEDIUM", "MEDIUM", "MEDIUM-TO-HIGH", "HIGH"
    ] = field(
        metadata={
            "description": "Estimated level of prospects' emotional excitement about getting the deal closed"
        }
    )
    intent_level: Literal[
        "UNDETERMINED", "LOW", "LOW-TO-MEDIUM", "MEDIUM", "MEDIUM-TO-HIGH", "HIGH"
    ] = field(
        metadata={
            "description": "Estimated level of prospects' expressed rational intent to get the deal closed"
        }
    )
    probability_of_closing: Literal[
        "UNDETERMINED", "LOW", "LOW-TO-MEDIUM", "MEDIUM", "MEDIUM-TO-HIGH", "HIGH"
    ] = field(
        metadata={
            "description": "Estimated probability of the deal eventually successfully closing, considering prospects' intent, excitement, responsiveness"
        }
    )
    time_to_close: Literal["UNDETERMINED", "IN_DAYS", "IN_WEEKS", "IN_MONTHS"] = field(
        metadata={
            "description": "Estimated time to closing the deal, considering prospects' excitement, intent, and probability of deal closing"
        }
    )


def main():
    merlin_model = OpenAIEnumModel(Color)
    #merlin_parser = OpenAIModel(Record)
    #print(f"enum model as prompt (explain=True): \n{merlin_model.as_prompt('grass')}")
    #print(f"parser as prompt: \n{merlin_parser.as_prompt('grass')}")

    #print(OpenAIModel(ParsedDeal).as_prompt("grass"))

    print(merlin_model("grass"))
    print(merlin_model.as_prompt("sea"))
    # print(Color("blood"))


if __name__ == "__main__":
    main()
