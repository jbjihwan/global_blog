# -*- coding: utf-8 -*-
import sys

def check():
    for pkg in ['google.analytics.data_v1beta', 'googleapiclient.discovery', 'google.oauth2.service_account']:
        try:
            __import__(pkg)
            print(f"[INSTALLED] {pkg}")
        except ImportError as e:
            print(f"[MISSING] {pkg}: {e}")

if __name__ == '__main__':
    check()
