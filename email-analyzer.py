#!/usr/bin/env python3

from email import message_from_string
from email.parser import HeaderParser
import pyfiglet
from argparse import ArgumentParser
import sys
import hashlib

SUPPORTED_FILE_TYPES = ["eml"]

def get_headers(mail_data : str):
    '''Get & Print Headers from mail data'''
    print(pyfiglet.figlet_format("Headers")) # Print Banner
    # Get Headers from mail data
    headers = HeaderParser().parsestr(mail_data, headersonly=True)
    # Print Headers
    for key,val in headers.items():
        print("_"*70)
        print(key+":")
        print(val)
        print("_"*70)

def get_digests(mail_data : str, filename : str):
    '''Get & Print Hash value of mail'''
    with open(filename, 'rb') as f:
        file        = f.read()
        file_md5    = hashlib.md5(file).hexdigest()
        file_sha1   = hashlib.sha1(file).hexdigest()
        file_sha256 = hashlib.sha256(file).hexdigest()
    
    digests = {
        "File MD5":file_md5,
        "File SHA1":file_sha1,
        "File SHA256":file_sha256,
        "Content MD5":hashlib.md5(mail_data.encode("utf-8")).hexdigest(),
        "Content SHA1":hashlib.sha1(mail_data.encode("utf-8")).hexdigest(),
        "Content SHA256":hashlib.sha256(mail_data.encode("utf-8")).hexdigest()
    }

    print(pyfiglet.figlet_format("Digests")) # Print Banner
    # Print digests
    for key,val in digests.items():
        print("_"*70)
        print(key+":")
        print(val)
        print("_"*70)

# Main
if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        "-f",
        "--filename", 
        type=str, 
        help="Name of file", 
        required=True
    )
    parser.add_argument(
        "-H",
        "--headers",
        help="Headers of the eml file", 
        required=False,
        action="store_true"
    )
    parser.add_argument(
        "-d",
        "--digests",
        help="Digests of the eml file", 
        required=False,
        action="store_true"
    )
    args = parser.parse_args()

    # Filename
    if args.filename:
        # Get Filename
        filename = str(args.filename)
        # Get File Format
        file_format = filename.split('.')[-1]
        if not file_format in SUPPORTED_FILE_TYPES:
            print("{} file format not supported".format(file_format))
            sys.exit(-1) #Exit with error code
    
    with open(filename,"r",encoding="utf-8") as file:
        data = file.read().rstrip()

    # Headers
    if args.headers:
        # Get & Print Headers
        get_headers(data)
    
    # Digests
    if args.digests:
        # Get & Print Digests
        get_digests(data,filename)
