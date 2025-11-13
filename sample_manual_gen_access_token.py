"""
Copyright (c) 2025 S V SUDHARSHAN a.k.a PriceCatch.
visit http://github.com/PriceCatch.

This code is part of the PRICECATCH CHARTS project and is
licensed under the Creative Commons Attribution 4.0 International License.
To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/.

Attribution:
When using this code in your project, please attribute it as follows:
- The first two lines must be placed in comments at the header of your code.
- If you are adding the code in a webpage, then, place the below phrase in the footer section
  of the webpage.
  PriceCatch Charts by S V SUDHARSHAN a.k.a PriceCatch is licensed under CC BY 4.0
"""
# Import the required module from the fyers_apiv3 package
import webbrowser
from fyers_apiv3 import fyersModel
#

# --------------- MOdify below statement and define the full path to the Opera executable on YOUR PC
opera_path = r"C:\Users\svsud\AppData\Local\Programs\Opera\opera.exe"

# Register the Opera browser using its full path
# The first argument is the name you want to use for this browser ('opera' is a good choice).
# The third argument is the BackgroundBrowser object with the executable path.
webbrowser.register('opera', None, webbrowser.BackgroundBrowser(opera_path))

# --------------- Modify below statements and define YOUR OWN Fyers API credentials
client_id = ""  # YOUR client id
secret_key = "" # YOUR secret key

redirect_uri = "https://trade.fyers.in/api-login/redirect-uri/index.html"
response_type = "code"
grant_type = "authorization_code"
state = "sample"

appSession = fyersModel.SessionModel(client_id=client_id, redirect_uri=redirect_uri, response_type=response_type, state=state,
                                     secret_key=secret_key, grant_type=grant_type)

# Construct the full URL
url_a = 'https://api-t1.fyers.in/api/v3/generate-authcode?'
url_b = 'client_id=' + client_id
url_c = '&redirect_uri=https://trade.fyers.in/api-login/redirect-uri/index.html&response_type=code&state=None'
full_url = url_a + url_b + url_c

# Get the registered Opera browser controller
opera_browser = webbrowser.get('opera')

# Open the URL using the specified browser
opera_browser.open(full_url)

auth_code = input("Auth Code ")
appSession.set_token(auth_code)
response = appSession.generate_token()

access_token = ""
try:
    access_token = response["access_token"]
except Exception as e:
    print(e, response)

# store access_token in a text file.
ACCESS_TOKEN_FILE = "C:/Users/svsud/Downloads/fyers_access_token.txt"
with open(ACCESS_TOKEN_FILE, "w") as access_tokenFile:
    access_tokenFile.write(access_token)

print("Done.")
# EOF
