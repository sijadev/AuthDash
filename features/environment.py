# test_project/features/environment.py
from test_framework.core.environment import setup_driver, teardown_driver

def before_all(context):
    setup_driver(context)

def after_all(context):
    teardown_driver(context)