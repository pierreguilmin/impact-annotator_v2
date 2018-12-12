from IPython.display import Markdown, display
import pandas as pd

def print_md(string, color=None):
    """
    Print markdown string in the notebook
    → Arguments:
        - string: string to print ('\t' is replaced by a tabulation, '\n' is replaced by a line break)
        - color : if specified prints the whole string with the given color
    """
    # replace '\t' and '\n' by their markdowns equivalent
    string = string.replace('\t', '&emsp;')
    string = string.replace('\n', '<br>')

    # use html tags to specify the string color
    if color:
        string = '<span style="color:{}">{}</span>'.format(color, string)

    display(Markdown(string))


def print_count(numerator, denominator):
    """
    Print custom string of the proportion numerator / denominator
    → Ex: print_count(5, 12) ⟹ '5/12 (41.067%)'
    → Arguments:
        - numerator  : numerator value
        - denominator: denominator value, should not be null
    """
    print('{}/{} ({:.2f}%)'.format(numerator,
                                   denominator,
                                   100 * numerator / denominator))


def unlist(nested_list):
    """
    Return the unnested version of a nested list (nested depth being not more than one)
    → Ex: unlist([[1, 2], [3, 4]]) ⟹ [1, 2, 3, 4]
    → Arguments:
        - nested_list: nested list
    """
    return [x for sublist in nested_list for x in sublist]


def get_table(data):
    """
    Return a count and frequency table of a categorical pandas Serie
    → Arguments:
        - data: categorical pandas Serie
    """
    # get the count and convert to dataframe
    table = pd.DataFrame(data={'count_': data.value_counts()})

    # create the frequency column and convert to a string like '52.3%'
    total_count = table['count_'].sum()
    table['freq_'] = table.apply(lambda x: '{:.2f}%'.format(100 * x['count_'] / total_count), axis=1)
    
    return table
