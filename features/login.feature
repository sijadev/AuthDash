Feature: Login-Funktion

  Scenario: Erfolgreiches Login
    Given die Loginseite ist geöffnet
    When der Benutzer sich mit "simon" und Passwort "23Sjge72!" anmeldet
    Then sieht der Benutzer das Dashboard