import csv

# ADJUST for source documents
# Define source of input files
input1_source = "CDC"
input2_source = "SSA"

# Define output file directory (relative to main script)
output_dir = 'MGT/Outputs/'

# open .tsv file(s)
#nih_initial = open('NIH_testing.tsv', encoding='utf-8').read().split('\n')
input1_initial = open('\GitHub\markXLIX.github.io\MGT\CDC_#_a.tsv',
                      encoding='utf-8').read().split('\n')
input2_initial = open('\GitHub\markXLIX.github.io\MGT\A_SSA English-Spanish.tsv',
                      encoding='utf-8').read().split('\n')
# END ADJUST for source documents

# COMMENTS
# Pandas caused type errors due to identifying some content as integer rather than string.
# Obviously can fix this but decided to just get it working as a normal list
# Probably just required encoding on read.  will have to test if time permits.
# Might be able to use the Google API to do this all within Google Sheets (without manual TSV export/import)
#cdc_list = pd.read_csv('CDC_testing.tsv', sep='\t', header=None)
#nih_list = pd.read_csv('NIH_testing.tsv', sep='\t', header=None)
# END COMMENTS

# Enhancements:
# trim leading and trailing spaces from the input items (causing errors in comparison)


#            <style>.row_highlight {background-color: gray;}</style>

def single_sheet_html(headers, no_match_list_input1_item, no_match_list_input2_item, terms_match, input1_count, input2_count, match_count, spanish_mismatch_count):
    html_start = f"""<html lang='en'>
            <meta charset='UTF-8'>
            <title>Multilingual Glossary Tool Diff of Glossaries - {input1_source} and {input2_source}</title>
            <meta name='viewport' content='width=device-width,initial-scale=1'>
            <head><link rel="stylesheet"  type="text/css" href="..\DiffMGT.css"></head>
            <body>
                <h1 class='TOP'>Multilingual Glossary Tool Diff of Glossaries</h1>
                """
    html_counter = single_sheet_html_count(
        input1_count, input2_count, match_count, spanish_mismatch_count)
    html_body = single_sheet_html_body(
        headers, no_match_list_input1_item, no_match_list_input2_item, terms_match)
    html_end = f"""
            </body>
        </html>"""
    return html_start + html_counter + html_body + html_end


def single_sheet_html_count(input1_count, input2_count, match_count, spanish_mismatch_count):
    html = f"""<div id='outline'>
        <p>
                <ul>
                    <li><a href='#input1_no_match'>{input1_source} English - No Match to {input2_source} English</a> - {input1_count} hits</li>
                    <li><a href='#input2_no_match'>{input2_source} English - No Match to {input1_source} English</a> - {input2_count} hits</li>
                    <li><a href='#match'>Inputs Match</a> - {match_count} hits</li>
                    <li><a href='#spanish_mismatch'>English Match, Spanish Does Not</a> - {spanish_mismatch_count} hits</li>

                </ul>
            </p>
    </div>"""
    return html

#DEBUG - This is not working


def single_sheet_html_body(headers, no_match_list_input1_item, no_match_list_input2_item, terms_match):
    # Input 1 vs Input 2
    table_1 = f"""<div id='input1_no_match'><h2>{input1_source} English - No Match to {input2_source} English</h2>
        <table><tr><th>{headers[0]}</th><th>{headers[1]}</th><th>{headers[2]}</th><th>{headers[3]}</th></tr>"""
    counter = 0
    highlight = ''
    for row in no_match_list_input1_item:
        # only highlight the odd rows
        if (counter % 2 == 0):
            highlight = "class='row_highlight'"
        term_row = f"""<tr {highlight}><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td></tr>"""
        table_1 = table_1 + term_row
        counter += 1
        highlight = ''
    table_1 += "</table><p><a href='#TOP'>Return to TOP</a></p><br/<br/></div>"
    # reset counter for next table
    counter = 0

    # input 2 vs Input 1
    table_2 = f"""<div id='input2_no_match'><h2>{input2_source} English - No Match to {input1_source} English</h2>
        <table><tr><th>{headers[0]}</th><th>{headers[1]}</th><th>{headers[2]}</th><th>{headers[3]}</th></tr>"""
    counter = 0
    highlight = ''
    for row in no_match_list_input2_item:
        # only highlight the odd rows
        if (counter % 2 == 0):
            highlight = "class='row_highlight'"
        term_row = f"""<tr {highlight}><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td></tr>"""
        table_2 = table_2 + term_row
        counter += 1
        highlight = ''
    table_2 += "</table><p><a href='#TOP'>Return to TOP</a></p><br/<br/></div>"
    # reset counter for next table
    counter = 0

    # Matches
    table_3 = f"""<div id='match'><h2>Inputs Match</h2>
        <table><tr><th>{headers[0]}</th><th>{headers[1]}</th><th>{headers[2]}</th><th>{headers[3]}</th></tr>"""
    counter = 0
    highlight = ''
    for row in terms_match:
        # only highlight the odd rows
        if (counter % 2 == 0):
            highlight = "class='row_highlight'"
        term_row = f"""<tr {highlight}><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td></tr>"""
        table_3 = table_3 + term_row
        counter += 1
        highlight = ''
    table_3 += "</table><p><a href='#TOP'>Return to TOP</a></p><br/<br/></div>"
    # reset counter for next table
    counter = 0

    table_4 = f"""<div id='spanish_mismatch'><h2>English Match, Spanish Does Not</h2>
        <table><tr><th>{headers[0]}</th><th>{headers[1]}</th><th>{headers[2]}</th><th>{headers[3]}</th></tr>"""
    counter = 0
    highlight = ''
    for row in spanish_mismatch:
        # only highlight the odd rows
        if (counter % 2 == 0):
            highlight = "class='row_highlight'"
        term_row = f"""<tr {highlight}><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td></tr>"""
        table_4 = table_4 + term_row
        counter += 1
        highlight = ''
    table_4 += "</table><p><a href='#TOP'>Return to TOP</a></p><br/<br/></div>"
    # reset counter for next table
    counter = 0

    return table_3 + table_4 + table_1 + table_2


input2_list = []
input1_list = []

for i in input1_initial:
    input1_list.append(i.split('\t'))
for i in input2_initial:
    input2_list.append(i.split('\t'))

# create empty variables to store results
terms_match = []
spanish_mismatch = []
no_match_list_input1_item = []
no_match_list_input2_item = []
last_english_term_input1_item = ''
last_english_term_input2_item = ''

# loop through each row in list1
for input1_item in input1_list:
    # assign value to last_english_term_cdc if current cdc value is non-empty.
    # otherwise do not change value of last_english_term_cdc
    if input1_item[0] != '':
        last_english_term_input1_item = input1_item[0]
    else:
        input1_item[0] = last_english_term_input1_item
    match_found = False
    # get length of inner list
    input2_list_len = len(input2_list)
    # loop through each row in list2
    for input2_item in input2_list:
        # create an index counter
        current_idx = input2_list.index(input2_item)
        # assign value to last_english_term_input2_item if current input2_item value is non-empty.
        # otherwise do not change value of last_english_term_input2_item
        if input2_item[0] != '':
            last_english_term_input2_item = input2_item[0]
        else:
            input2_item[0] = last_english_term_input2_item
        if input1_item == input2_item:
            # This means there is a matching English/Spanish term pair in each list
            terms_match.append(
                [input1_item[0], input1_item[1], input2_item[0], input2_item[1]])
            # break out of the loop through list2
            match_found = True
            input2_list.remove(input2_item)
            break
        elif input1_item[0] == input2_item[0]:
            spanish_mismatch.append([input1_item[0], input1_item[1],
                                     input2_item[0], input2_item[1]])
            match_found = True
            input2_list.remove(input2_item)
            break
    if not match_found:
        no_match_list_input1_item.append(
            [input1_item[0], input1_item[1], None, None])

# Remaining items in second list do not have a match in the first list.  Simply output
for input2_item in input2_list:
    no_match_list_input2_item.append(
        [None, None, input2_item[0], input2_item[1]])

# Check for SSA terms that do not exist in CDC list
""" for input2_item in input2_list:
    match_found = False
    for input1_item in input1_list:
        if input1_item[0] != '':
            last_english_term_input1_item = input1_item[0]
        else:
            input1_item[0] = last_english_term_input1_item
        match_found = False
        # check if the first item in the row matches (this means there is a matching English term in each list)
        if input2_item[0] == input1_item[0]:
            # check if the second item in the row matches (This means there is a matching Spanish term in each list)
            if input2_item[1] == input1_item[1]:
                # Do not output this value as it has already been found in the first loop (compare input1 to input2)
                match_found = True
                break
    if not match_found:
        a = [None, None, input2_item[0], input2_item[1]]
        no_match_list_input2_item.append(a) """

# count of each output variable
count_no_match_list_input1 = len(no_match_list_input1_item)
count_no_match_list_input2 = len(no_match_list_input2_item)
count_terms_match = len(terms_match)
count_spanish_mismatch = len(spanish_mismatch)

# print the results to screen DEBUG
""" print("\n", input1_source,
      "English/Spanish pair does not exist in", input2_source, ": ")
for row in no_match_list_input1_item:
    print(row)
print("No match count:", count_no_match_list_input1)

print("\n", input2_source,
      "English/Spanish pair does not exist in", input1_source, ": ")
for row in no_match_list_input2_item:
    print(row)
print("No match count:", count_no_match_list_input2)

print("\nEnglish and Spanish Terms Match:")
for row in terms_match:
    print(row)
print("Match count:", count_terms_match) """

# headers
headers = ['CDC English', 'CDC Spanish', 'SSA English', 'SSA Spanish']

# names of files to write
MGT_Diff_Single_Sheet_HTML = output_dir + input1_source + '_' + \
    input2_source + '__' + 'MGTDiffSingleSheet.html'

# write the files
with open(MGT_Diff_Single_Sheet_HTML, 'wt', encoding='utf-8', newline='') as file_out:
    html = single_sheet_html(headers, no_match_list_input1_item, no_match_list_input2_item, terms_match,
                             count_no_match_list_input1, count_no_match_list_input2, count_terms_match, count_spanish_mismatch)
    file_out.write(html)
