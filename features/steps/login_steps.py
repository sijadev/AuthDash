from behave import given, when, then
from test_framework.keywords.login_keywords import open_login_page, login_as_user, verify_dashboard

@given("die Loginseite ist geöffnet")
def step_open(context):
    open_login_page(context.driver)

@when('der Benutzer sich mit "{username}" und Passwort "{password}" anmeldet')
def step_login(context, username, password):
    login_as_user(context.driver, username, password)

@then("sieht der Benutzer das Dashboard")
def step_dashboard(context):
    verify_dashboard(context.driver)