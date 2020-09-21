from bs4 import BeautifulSoup
import requests


website_url = "https://etablissements.fhf.fr"
directory_endpoint = "annuaire/"


def get_soup(url):
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')
    return soup


def get_fiches(url):
    soup = get_soup(url)

    fiches = []
    for a in soup.find_all('a', href=True):
        if a['href'].startswith("hopital-fiche"):
            fiches.append(a['href'])
    return fiches


# Get emails
def get_emails(fiches):
    emails = []

    for fiche in fiches:
        url = "{}/{}{}".format(website_url, directory_endpoint, fiche)
        soup = get_soup(url)
        print("Scrapping ", url)
        mail = soup.find('span', attrs={'class':'courriel'})
        if mail is not None:
            output = mail.text.split()[-1]
            emails.append(output.strip())
    return emails


def two_dimensional_array_to_list(array):
    res = []

    for x in array:
        for y in x:
            res.append(y)
    return res


def do_pages(fiches, emails):
    i = 4

    while True:
        soup = get_soup("{}/{}vie-hopitaux.php?item=mouvements&page={}".format(website_url, directory_endpoint, i))
        next_page = soup.find('a', attrs={'class': 'next'}, href=True)

        if next_page is not None and next_page['href'] and next_page['href'] != "#":
            fiches.append(get_fiches(website_url + next_page['href']))
            i += 1
        else:
            break
    fiches = two_dimensional_array_to_list(fiches)
    fiches = list(dict.fromkeys(fiches))
    emails.append(get_emails(fiches))


def write_output(emails):
    # Remove duplicate
    emails = two_dimensional_array_to_list(emails)
    print(emails)
    emails = list(dict.fromkeys(emails))

    # Write in output.txt
    f = open("output.txt", "a")
    f.seek(0)
    f.truncate()
    f.write("\n".join(emails))
    f.close()


def main():
    fiches = []
    emails = []
    do_pages(fiches, emails)
    write_output(emails)


if __name__ == '__main__':
    main()
