import os
import logging

from github import Auth
from github import Github


logging.basicConfig(
    format=r'%(levelname)s [%(asctime)s]: "%(message)s"',
    datefmt=r'%Y-%m-%d %H:%M:%S', level=logging.DEBUG
)

client = Github(auth=Auth.Token(os.environ.get("GITHUB_TOKEN", "")))
