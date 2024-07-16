import queries
import json

from dotenv import dotenv_values

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

import queries.sample

ENV_FILE=".env"
FFLOGS_URL="https://www.fflogs.com/api/v2/client"
FFLOGS_TOKEN_URL="https://www.fflogs.com/oauth/token"

def main():
    config = dotenv_values(ENV_FILE)
    client_id, client_secret = '', ''
    if 'CLIENT_ID' in config.keys():
        client_id = config['CLIENT_ID']
    if 'CLIENT_SECRET' in config.keys():
        client_secret = config['CLIENT_SECRET']

    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)

    token = oauth.fetch_token(
        token_url=FFLOGS_TOKEN_URL,
        client_id=client_id,
        client_secret=client_secret,
    )

    headers = {
        "Content-Type":"application/json",
        "Authorization": f"Bearer {token['access_token']}"
    }

    transport = AIOHTTPTransport(url=FFLOGS_URL, headers=headers)
    gql_client = Client(transport=transport, fetch_schema_from_transport=True)

    response=gql_client.execute(queries.sample.QUERY)

    with open("sample.json", "w") as out_file:
        json.dump(response, out_file)

    events = response['reportData']['report']['events']['data']
    actors = response['reportData']['report']['masterData']['actors']

    for event in events:
        if 'sourceID' in event.keys():
            for actor in actors:
                if actor['id'] == event['sourceID']:
                    event['sourceID'] = actor['name']
        if 'targetID' in event.keys():
            for actor in actors:
                if actor['id'] == event['targetID']:
                    event['targetID'] = actor['name']

    with open("cleaned_sample.json", "w") as out_file:
        json.dump(events, out_file)


    ability_types = set()
    for event in events:
        if "type" in event.keys():
            ability_types.add(event['type'])
            if event['type'] == 'heal':
                print(event)



if __name__ == "__main__":
    main()