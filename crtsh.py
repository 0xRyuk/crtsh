# This script is used to find subdomains of a given domain.
# It uses the crtsh API to get information about the subdomains of a domain
# and then displays them in a formatted table.

import requests
import argparse
import sys
import json
import platform
from colorama import init, Fore, Style
from prettytable import PrettyTable

# initialize colorama if on Windows
if platform.system() == "Windows":
    init(convert=True)

epilog = ""

banner = [
    """
      ::::::::  ::::::::: :::::::::::     ::::::::  :::    ::: 
    :+:    :+: :+:    :+:    :+:        :+:    :+: :+:    :+:  
   +:+        +:+    +:+    +:+        +:+        +:+    +:+   
  +#+        +#++:++#:     +#+        +#++:++#++ +#++:++#++    
 +#+        +#+    +#+    +#+               +#+ +#+    +#+     
#+#    #+# #+#    #+#    #+#    #+# #+#    #+# #+#    #+#      
########  ###    ###    ###    ###  ########  ###    ###  v1.0 beta 
""",
    """
                                    [Github  : 0xRyuk]  
                                    [Twitter : 0xRyuk]
""",
    f"{Fore.BLUE}┌──{Fore.RED}[{Fore.GREEN}Enter your target {Style.RESET_ALL}'eg: {Fore.LIGHTRED_EX}hackerone{Style.RESET_ALL} or {Fore.LIGHTRED_EX}hackerone.com{Style.RESET_ALL}'{Fore.RED}]{Fore.BLUE}~{Fore.GREEN}:{Style.RESET_ALL}",
    f"{Fore.BLUE}└╼{Fore.RED}#{Style.RESET_ALL}",
]

# initialize the argument parser
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    usage=f'crtsh -t "hackerone.com" [options]',
    epilog=epilog,
    add_help=False,
)

# options to the argument parser
parser.add_argument_group("Options")

parser.add_argument(
    "-h ",
    "--help",
    action="store_true",
    default=False,
    help="Show usage and help options",
)
parser.add_argument("-t", "--target", dest="target", metavar="", help="Search target")
parser.add_argument(
    "-o", "--out", dest="output", metavar="", help="Output file", default=False
)
parser.add_argument(
    "-p ",
    "--plain",
    action="store_true",
    default=False,
    help="Plain output, useful for piping result [Default: formatted]",
)

args = parser.parse_args()

domain = args.target
output = args.output

subdomains = set()
wildcard_domains = set()


def crtsh(domain):
    """
    Finds subdomains of the given domain by using the certificate transparency logs search service provided by crt.sh.

    Sends a HTTP GET request to crt.sh with the specified domain as a query parameter, and parses the JSON response to extract the subdomains.

    Args:
        domain (str): The domain to find subdomains of.

    Returns:
        None
    """
    try:
        url = "https://crt.sh"
        query = {"q": domain, "output": "json"}
        response = requests.get(url, params=query, timeout=20)

        if response.ok:
            data = response.content.decode("UTF-8")
            jsondata = json.loads(data)
            for item in range(len(jsondata)):
                domain = jsondata[item]["name_value"]  # getting domains
                for subdomain in domain.split("\n"):
                    if subdomain.find("*"):
                        subdomains.add(subdomain)
                    else:
                        if subdomain not in wildcard_domains:
                            wildcard_domains.add(subdomain)
    except Exception as e:
        print(e)


def save(data, output):
    """
    Saves the given data to the specified output file.

    If the output file does not have a '.txt' extension, it is added automatically.

    Args:
        data (list): The data to be saved.
        output (str): The path of the output file.
    """
    try:
        if ".txt" not in output:
            output += ".txt"
        with open(output, "w") as file1:
            for subdomain in data:
                file1.write(subdomain + "\n")
        file1.close()

        with open(f"wildcard-{output}", "w") as file2:
            for wildcard in wildcard_domains:
                file2.write(wildcard + "\n")

        file2.close()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    try:
        # Set up formatting for bannner and interactive shell
        print(Fore.GREEN + banner[0])
        print(Fore.LIGHTMAGENTA_EX + banner[1] + Style.RESET_ALL)
         # Check if the --help flag was passed
        if args.help:
            parser.print_help()
            sys.exit()

        # Check if the domain was passed as a command-line argument
        # or entered interactively
        if not domain:
            print(banner[2])
            print(banner[3], end="")
            domain = str(input())

        # Get subdomains from the crtsh API
        print(f"\nGetting info from '{Fore.GREEN}https://crt.sh{Style.RESET_ALL}'\n")
        crtsh(domain)

        if output:
            save(subdomains, output)

        # Check if the --plain flag was passed and print simple subdomains and exit with status 0
        if args.plain:
            for sub in subdomains:
                print(sub)
            sys.exit(0)
        # Create a formatted table of subdomains
        myTable = PrettyTable(
            [
                Fore.LIGHTYELLOW_EX + "No." + Style.RESET_ALL,
                Fore.LIGHTYELLOW_EX + "Wildcard Domain" + Style.RESET_ALL,
                Fore.LIGHTYELLOW_EX + "Subdomain" + Style.RESET_ALL,
            ]
        )
        for index, item in enumerate(subdomains):
            if index < len(wildcard_domains):
                myTable.add_row(
                    [
                        index + 1,
                        Fore.LIGHTRED_EX
                        + list(wildcard_domains)[index]
                        + Style.RESET_ALL,
                        Fore.LIGHTGREEN_EX + item + Style.RESET_ALL,
                    ]
                )
            else:
                myTable.add_row(
                    [index + 1, "", Fore.LIGHTGREEN_EX + item + Style.RESET_ALL]
                )
        myTable.align = "l"
        print(myTable)
    except Exception as e:
        print(Fore.YELLOW + e + Style.RESET_ALL)
    except KeyboardInterrupt:
        print(Fore.RED + "\nExiting..")
