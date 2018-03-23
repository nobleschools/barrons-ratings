
"""
The program takes a folder full of HTML files and
takes the college name and selectivity of each college,
and then  writes that information to a spreadsheet.
"""

import os, bs4, csv, itertools

DATADIR = "/home/pi/projects/barrons/data/downs_full"
DEFAULT_NO_COMP = "Not Available"


def main():
    """
    Scrapes each html file for college
    name and competitivenes rating.
    """
    csvFile = open('college.csv', 'w', newline='')
    csvWriter = create_csvWriter(csvFile)
    input_files_names = os.listdir(DATADIR)
    print("starting")
    for file_name in input_files_names:
        if file_name.endswith(".html"):
            print(".", end="", flush=True)
            soup = create_soup(file_name)
            name = college_names(soup)
            if name is None:
                continue
            selectivity = competitivenes(soup)

        csvWriter.writerow([name, selectivity, file_name])
    print("Finished")
    csvFile.close()


def create_soup(file_name):
    """
    Opens one HTML file and creates
    a soup object for that file.

    Parameters:
    - file_name - string, path
      to a barrons html file.

    Return Type:
    - bs4.BeautifulSoup object.
    """
    file = (os.path.join(DATADIR, file_name))
    pull_barrons_infoFile = open(file, 'r')
    pull_barrons_infoContent = pull_barrons_infoFile.read()
    pull_barrons_infoSoup = bs4.BeautifulSoup(
        pull_barrons_infoContent, "html.parser"
    )
    return pull_barrons_infoSoup



def college_names(soup):
    """
        Takes the college name value
        from the BeautifulSoup object.

        College name is found
        as the last th element.

        Parameters:
        - soup - bs4.BeautifulSoup object.

        Return Type:
        - String, school_name.
    """

    th_elements = soup.select('html #search-profile #page-wrapper div#content-wrapper div#searchleftcol div.searchcontent table.tbl-profile tbody.basic-info tr th')
    try:
        school_name = th_elements[-1].text
        '''For a handfull of files, a semicolon is not
           present in the html file, but gets inserted.'''
        school_name = school_name.replace(";", "")
    except IndexError:
        return None

    return school_name


def competitivenes(soup):
    """
        Takes the selectivity rating
        from the BeautifulSoup object.

        Parameters:
        - soup - bs4.BeautifulSoup object.

        Return Type:
        - String object, competitivenes.

    """
    td_elements = soup.select('html #search-profile #page-wrapper #content-wrapper #searchleftcol div table tbody.basic-info tr td')

    try:
        competitivenes = td_elements[-1].text

    except IndexError:
        '''
        Some files do not have a
        competitivenes rating
        '''
        print("Not Available")
        competitivenes = None
    if competitivenes == " ":
        competitivenes = DEFAULT_NO_COMP

    '''Some files only had an ACT as final list object.
       No other competitivesnes rating available.'''

    elif competitivenes.startswith("ACT:"):
        competitivenes = DEFAULT_NO_COMP
    return competitivenes



def create_csvWriter(csvFile):
    """
    Generates the spreadsheet,
    and writes the header row.

    Parameter:
    - csvFile, os.File, the file in which the
    spreedsheet will be generated in.

    Return Type:
    - csv.Writer

    """
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(['College Name', 'Selectivity', 'file_name'])
    return csvWriter


if __name__ == "__main__":
    main()

