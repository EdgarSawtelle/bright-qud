"""Paper doll stand-in base body (B3 figure without sash). doll_body.py may redefine "body/base"."""
from b3kit import person

LAYERS = {"body/base": [row.replace("x", ".") for row in person(face="face", sash=False)]}
