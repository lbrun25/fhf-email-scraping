# fhf-email-scraping

This script scrapes email addresses from the FHF (Fédération hospitalière de France) directory (https://etablissements.fhf.fr/annuaire/). It can scrape emails either from nomination pages or by iterating over institution fiches by ID.

## Disclaimer

This script is for learning purpose only. Do not use the emails to spam people or sell them.

## Usage

You can run `python3 main.py -h` to display the usage instructions for the script.

You can run `python3 main.py --mode 1` to scrap emails from nomination pages or `python3 main.py --mode 2` to scrap emails from fiches.

Then, The emails that are scraped are saved in the file `output.txt`. Please note that the content of this file is deleted each time the script is launched.

### Nomination pages

You can scrap emails from nomination pages. It will scrape emails from pages starting at https://etablissements.fhf.fr/annuaire/vie-hopitaux.php?item=mouvements&page=1.

Run `python3 main.py --mode 1`

You can use the --sleep argument to specify a delay (in seconds) between each scraped page. The default value is 2 seconds.
For example, you can run `python3 main.py --mode 1 --sleep 5`.

### Fiches

You can scrap emails by iterating through a list of institution by providing an ID range. For example, when the id is 2, it will scrape the email from this page: https://etablissements.fhf.fr/annuaire/hopital-fiche.php?id=2.
This method may not be effective as some institutions may not be listed or may no longer be in operation, but you can still scrape many emails by browsing the records by id.

You can specify a range for the IDs to iterate by using the `--lower` and `--upper` arguments. The default range is from 0 to 10000.

To iterate through IDs from 3000 to 5000, run `python3 main.py --mode 2 --lower 3000 --upper 5000`.

You can use the --sleep argument to specify a delay (in seconds) between each scraped page. The default value is 2 seconds.
For example, you can run `python3 main.py --mode 2 --sleep 5`.

If an error occurs, you can retry the operation up to three times on the same record with a 10-second delay between attempts.
Use the `--retry` flag to enable retries. By default, retries are disabled.

For example, you can run `python3 main.py --mode 2 --lower 3000 --upper 5000 --sleep 0.2 --retry`

## Installation

### Create virtual env

Run virtualenv venv to create your environment:
`python3 -m venv .venv`

### Activate the virtual environment

#### On Unix or macOS, using the bash shell
Run: `source .venv/bin/activate`

#### On Unix or macOS, using the csh shell
Run: `source .venv/bin/activate.csh`

#### On Unix or macOS, using the fish shell
Run: `source .venv/bin/activate.fish`

#### On Windows using the Command Prompt
Run: `.venv\Scripts\activate.bat`

#### On Windows using PowerShell:
Run: `.venv\Scripts\Activate.ps1`

### Install dependencies
Run the following command to install packages in your virtual environment:
`pip install -r requirements.txt`
