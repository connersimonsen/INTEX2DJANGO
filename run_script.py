#!/usr/bin/env python3

# initialize django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'arcticapi.settings'
import django
django.setup()

# regular imports
from api.models import Campaign, Category
import json, csv, sys

# main script
def main():
    

# bootstrap
if __name__ == '__main__':
    main()
