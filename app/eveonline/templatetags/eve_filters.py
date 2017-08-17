from django import template
from django.template.defaultfilters import stringfilter
import re
register = template.Library()

# TODO: LEARN REGEX
@register.filter(name='humanReadable')
def humanReadable(value):
    pass
    # value = int(value)
    # value_as_string = str(value)
    # value_length = len(value_as_string)
    # leading_number_count = value_length % 3
    #
    # # Add leading numbers to output
    # if leading_number_count != 0:
    #     output = value_as_string[0:leading_number_count] + ","
    # else:
    #     output = ""
    #
    # stop_at_character = leading_number_count
    #
    # # Build output from remaining integers
    # number_pair_counter = stop_at_character + 3
    # number_pairs_total = (value_length - leading_number_count) / 3
    # for current_number_pair in range(0, number_pairs_total):
    #     output += value_as_string[stop_at_character:number_pair_counter]
    #     stop_at_character = number_pair_counter
    #     number_pair_counter += 3
    #     if not (current_number_pair == number_pairs_total - 1):
    #         output += ","
    # return output

@register.filter(name='cleanTypes')
def cleanTypes(string):
    string = string.split("_")
    cleaned_value = ""
    for data in string:
        cleaned_value += data.title() + " "
    return cleaned_value
