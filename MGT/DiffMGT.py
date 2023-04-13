import csv
# open .tsv file(s)

# DEBUG
# probably need to rename all the agency specific elements to something generic

#nih_initial = open('NIH_testing.tsv', encoding='utf-8').read().split('\n')
nih_initial = open('A_latinoschools_spanish_vocabulatory_Medicine_and_health.tsv',
                   encoding='utf-8').read().split('\n')
cdc_initial = open('CDC_testing.tsv', encoding='utf-8').read().split('\n')
# Pandas caused type errors due to identifying some content as integer rather than string.
# Obviously can fix this but decided to just get it working as a normal list
# Probably just required encoding on read.  will have to test if time permits.
# Might be able to use the Google API to do this all within Google Sheets (without manual TSV export/import)
#cdc_list = pd.read_csv('CDC_testing.tsv', sep='\t', header=None)
#nih_list = pd.read_csv('NIH_testing.tsv', sep='\t', header=None)

nih_list = []
cdc_list = []

for i in cdc_initial:
    cdc_list.append(i.split('\t'))
for i in nih_initial:
    nih_list.append(i.split('\t'))

# create empty variables to store results
terms_match = []
no_match_list_cdc = []
no_match_list_nih = []
english_term_exists = []
last_english_term_cdc = ''
last_english_term_nih = ''
cdc_counter = 0
nih_counter = 0

# loop through each row in list1
for cdc in cdc_list:
    nih_counter = 0
    # assign value to last_english_term_cdc if current cdc value is non-empty.
    # otherwise do not change value of last_english_term_cdc
    if cdc[0] != '':
        last_english_term_cdc = cdc[0]
    else:
        cdc[0] = last_english_term_cdc
    match_found = False
    # loop through each row in list2
    for nih in nih_list:
        # assign value to last_english_term_nih if current nih value is non-empty.
        # otherwise do not change value of last_english_term_nih
        if nih[0] != '':
            last_english_term_nih = nih[0]
        else:
            nih[0] = last_english_term_nih
        match_found = False
        # check if the first item in the row matches
        if cdc[0] == nih[0]:
            # check if the second item in the row matches
            if cdc[1] == nih[1]:
                # if there is a match, add the row to the match_list variable
                a = [cdc[0], cdc[1], nih[0], nih[1]]
                terms_match.append(a)
                # break out of the loop through list2
                match_found = True
                del nih_list[nih_counter]
                break
            else:
                a = [cdc[0], cdc[1], nih[0], nih[1]]
                english_term_exists.append(a)
                match_found = True
                del nih_list[nih_counter]
                break
        nih_counter += 1
    # if no match was found, add the row to the no_match_list variable
    if not match_found:
        a = [cdc[0], cdc[1], nih[0], nih[1]]
        no_match_list_cdc.append(a)
    cdc_counter += 1

# Check for NIH terms that do not exist in CDC list
for nih in nih_list:
    match_found = False
    for cdc in cdc_list:
        if nih[0] == cdc[0]:
            match_found = True
            break
    if not match_found:
        a = [cdc[0], cdc[1], nih[0], nih[1]]
        no_match_list_nih.append(a)

# count of each output variable
count_english_term_exists = len(english_term_exists)
count_no_match_list_cdc = len(no_match_list_cdc)
count_no_match_list_nih = len(no_match_list_nih)
count_terms_match = len(terms_match)

# print the results to screen
print("\nCDC English Terms Exists, Spanish Does Not Match:")
for row in english_term_exists:
    print(row)
print("Match count:", len(english_term_exists))

print("\nCDC English Term does not exist in NIH:")
for row in no_match_list_cdc:
    print(row)
print("No match count:", count_no_match_list_cdc)

print("\nNIH English Term does not exist in CDC:")
for row in no_match_list_nih:
    print(row)
print("No match count:", count_no_match_list_nih)

print("\nEnglish and Spanish Terms Match:")
for row in terms_match:
    print(row)
print("Match count:", count_terms_match)

# headers
headers = ['CDC English', 'CDC Spanish', 'NIH English', 'NIH Spanish']

# names of files to write to
English_Not_Spanish = 'EnglishNotSpanish.tsv'
CDC_English_Not_NIH_Spanish = 'CDCEnglishNotNIHSpanish.tsv'
CNIH_English_Not_CDC_Spanish = 'CNIHEnglishNotCDCSpanish.tsv'
Terms_Match = 'TermsMatch.tsv'
MGT_Diff_Single_Sheet = 'MGTDiffSingleSheet.tsv'

# write the TSV files
with open(MGT_Diff_Single_Sheet, 'wt', encoding='utf-8', newline='') as file_out:
    tsv_writer = csv.writer(file_out, delimiter='\t')
    tsv_writer.writerow([h for h in headers])
    tsv_writer.writerow(
        ["Count of CDC English matches NIH English but not Spanish: ", count_english_term_exists])
    tsv_writer.writerow(
        ["Count of CDC English has no NIH English Match: ", count_no_match_list_cdc])
    tsv_writer.writerow(
        ["Count of NIH English has no CDC English Match: ", count_no_match_list_nih])
    tsv_writer.writerow(
        ["Count CDC and NIH Terms that match Both English and Spanish: ", count_terms_match])
    for i in english_term_exists:
        a = ['1'] + i
        tsv_writer.writerow(a)
    for j in no_match_list_cdc:
        b = ['2'] + j
        tsv_writer.writerow(b)
    for k in no_match_list_nih:
        c = ['3'] + k
        tsv_writer.writerow(c)
    for l in terms_match:
        d = ['4'] + l
        tsv_writer.writerow(d)

with open(English_Not_Spanish, 'wt', encoding='utf-8', newline='') as file_out:
    tsv_writer = csv.writer(file_out, delimiter='\t')
    tsv_writer.writerow([h for h in headers])
    tsv_writer.writerow(["Count: ", count_english_term_exists])
    for i in english_term_exists:
        tsv_writer.writerow(i)

with open(CDC_English_Not_NIH_Spanish, 'wt', encoding='utf-8', newline='') as file_out:
    tsv_writer = csv.writer(file_out, delimiter='\t')
    tsv_writer.writerow([h for h in headers])
    tsv_writer.writerow(["Count: ", count_no_match_list_cdc])
    for i in no_match_list_cdc:
        tsv_writer.writerow(i)

with open(CNIH_English_Not_CDC_Spanish, 'wt', encoding='utf-8', newline='') as file_out:
    tsv_writer = csv.writer(file_out, delimiter='\t')
    tsv_writer.writerow([h for h in headers])
    tsv_writer.writerow(["Count: ", count_no_match_list_nih])
    for i in no_match_list_nih:
        tsv_writer.writerow(i)

with open(Terms_Match, 'wt', encoding='utf-8', newline='') as file_out:
    tsv_writer = csv.writer(file_out, delimiter='\t')
    tsv_writer.writerow([h for h in headers])
    tsv_writer.writerow(["Count: ", count_terms_match])
    for i in terms_match:
        tsv_writer.writerow(i)
