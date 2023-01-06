from bs4 import BeautifulSoup
import requests
import time
import sys
import argparse
from itertools import chain


website_url = "https://etablissements.fhf.fr"
directory_endpoint = "annuaire/"


class Config:
    mode: int
    startIndex: int
    endIndex: int
    sleepTime: float
    isRetry: bool


config = Config()


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
        time.sleep(config.sleepTime)
    return emails

# Do nomination pages https://etablissements.fhf.fr/annuaire/vie-hopitaux.php?item=mouvements&page=1
def do_nominations_pages(fiches, emails):
    i = 1
    is_last_page = 0

    while True:
        soup = get_soup("{}/{}vie-hopitaux.php?item=mouvements&page={}".format(website_url, directory_endpoint, i))
        next_page = soup.find('a', attrs={'class': 'next'}, href=True)

        print("Scrapping page {}".format(i))
        if next_page['href'] == "#":
            is_last_page += 1
        if next_page is not None and next_page['href'] and next_page['href'] != "#" and is_last_page <= 1:
            fiches.append(get_fiches(website_url + next_page['href']))
            i += 1
        else:
            break
        time.sleep(config.sleepTime)
    fiches = list(chain(*fiches))
    fiches = list(dict.fromkeys(fiches))
    emails.append(get_emails(fiches))
    emails = list(chain(*emails))


def write_output(emails):
    # Flatten multidimensional array
    emails = list(chain(*emails))
    # Remove duplicates
    emails = list(dict.fromkeys(emails))

    # Write in output.txt
    f = open("output.txt", "a")
    f.seek(0)
    f.truncate()
    f.write("\n".join(emails).lower())
    f.close()


# Do fiches https://etablissements.fhf.fr/annuaire/hopital-fiche.php?id=2
def do_fiches(emails):
    i = config.startIndex
    notExistMsg = "This establishment does not exist or no longer exists."
    retry = 0

    while i < config.endIndex:
        fiche = "hopital-fiche.php?id={}".format(i)
        url = "{}/{}{}".format(website_url, directory_endpoint, fiche)
        try:
            print(url)
            soup = get_soup(url)
            result = soup.find("h1", attrs={"class":"intro_article"})

            if result.text.strip() != notExistMsg:
                mail = soup.find('span', attrs={'class':'courriel'})
                if mail is not None:
                    output = mail.text.split()[-1]
                    emails.append(output.strip())
        except Exception as e:
            print(e)
            if retry < 3 and config.isRetry:
                print("Retry...")
                retry += 1
                time.sleep(10)
                continue
        i += 1
        retry = 0
        time.sleep(config.sleepTime)


def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def main():
    fiches = []
    emails = []
    parser = argparse.ArgumentParser(description="Get some mail on https://etablissements.fhf.fr")
    parser.add_argument("--mode", required=True, help="1. Get emails from the nominations page\n2. Get emails by iterating fiche id", type=int)
    parser.add_argument("--lower", required=False, help="Start index", type=int, default=0)
    parser.add_argument("--upper", required=False, help="End index", type=int, default=10000)
    parser.add_argument("--sleep", required=False, help="Time to sleep between each request", type=float, default=2)
    parser.add_argument("--retry", required=False, help="Retry request if it failed", action=argparse.BooleanOptionalAction, default=False)

    args = parser.parse_args()
    config.mode = args.mode
    config.startIndex = args.lower
    config.endIndex = args.upper
    config.sleepTime = args.sleep
    config.isRetry = args.retry

    if config.mode == 1:
        do_nominations_pages(fiches, emails)
    elif config.mode == 2:
        if config.startIndex is None or config.endIndex is None:
            print("Please specify lower and upper bound to iterate fiche id pages.")
            sys.exit(1)
        else:
            do_fiches(emails)
    else:
        print("Unknown mode. Please select 1 or 2")
        sys.exit(1)
    write_output(emails)


if __name__ == '__main__':
    main()
