# msal-bearer
Python package to get auth token interactively for a msal public client application and cache it locally.

## Usage


````
tenantID = "YOUR_TENANT_ID"
client_id = "YOUR_CLIENT_ID"
scope = ["YOUR_SCOPE"]

auth = BearerAuth.get_bearer_token_auth(
    tenantID=tenantID,
    clientID=client_id,
    scopes=scope
)



NB! Delegated scopes should include client_id of where scope is from.

## Installing
Install using pip or poetry.

pip install bearerauth
