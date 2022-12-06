# crtsh

A simple command line utility to find subdomains of a given domain using the certificate transparency logs search service provided by crt.sh.

It fetches data from [crt.sh](https://crt.sh/) to get related subdomains and wildcards

## Installation

To install crtsh, clone the repository and run:
>pip install -r requirements.txt


To use this tool as linux command follow these steps

Create crtsh directory under /opt
>sudo mkdir -p /opt/crtsh

Copy python file to previously created directory
>sudo cp crtsh.py /opt/crtsh/

Pase below commands in terminal

>sudo echo 'alias crtsh="python3 /opt/crtsh/crtsh.py"'>>~/.zshrc

>sudo echo 'alias crtsh="python3 /opt/crtsh/crtsh.py"'>>~/.bashrc

Refrash terminal profile
>source ~/.zshrc

>source ~/.bashrc

Run with
>crtsh

or

>crtsh -t hackerone.com

# Usage
To find subdomains of a domain, use the -t or --target option followed by the domain name:

>crtsh -t "hackerone.com"

The subdomains will be displayed in a formatted table.

## Options
`crtsh` supports the following options:

```
-h, --help          Show usage and help options
-t, --target        Search target
-o, --out           Output file
-p, --plain         Plain output, useful for piping result [Default: formatted]
```
For example, to output the results to a file, use the `-o` or `--out ` option followed by the path to the file:

>crtsh -t "hackerone.com" -o "/path/to/file.txt"

### Pipe
Stdout to use with other tools
>crtsh -t hackerone.com -p | httpx

use the `-p` or `--plain` option to display the results in a normal format.



>cat domains.txt | crtsh

# Todo

- [ ] JSON Support

- [ ] Threading

- [x] Color formatted output for windows

- [ ] Enumerate multiple domains from file

- [ ] Logging