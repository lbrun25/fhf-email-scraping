from bs4 import BeautifulSoup
import requests

# Get fiches

url = "https://etablissements.fhf.fr/annuaire/vie-hopitaux.php?item=mouvements&page=1"
data = requests.get(url)
soup = BeautifulSoup(data.text, 'html.parser')
items = soup.find(id="liste-commnuniques")
item = items.find_all("li")

fiches = []
for a in soup.find_all('a', href=True):
    if a['href'].startswith("hopital-fiche"):
        fiches.append(a['href'])


# Get emails
emails = []

for fiche in fiches:
    url = "https://etablissements.fhf.fr/annuaire/" + fiche
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')
    mail = soup.find('span', attrs={'class':'courriel'})
    if mail is not None:
        output = mail.text.split()[-1]
        emails.append(output.strip())


# Remove duplicate
emails = list(dict.fromkeys(emails))


# Write in output.txt
f = open("output.txt", "a")
f.seek(0)
f.truncate()
for mail in emails:
    f.write(mail)
f.close()