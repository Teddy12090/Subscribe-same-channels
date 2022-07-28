import glob
from time import sleep
from typing import Set

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

scopes_youtube = ["https://www.googleapis.com/auth/youtube"]
client_secrets_file = next(glob.iglob("client_secret_*.apps.googleusercontent.com.json"))


def retrieve_all_subscriptions(youtube=None):
    if youtube is None:
        flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes_youtube)
        credentials = flow.run_local_server(port=8081)
        youtube = build("youtube", "v3", credentials=credentials)
    subscriptions = youtube.subscriptions().list(part="snippet,contentDetails", mine=True, maxResults=50).execute()
    result = [item for item in subscriptions["items"]]
    while "nextPageToken" in subscriptions:
        subscriptions = youtube.subscriptions().list(part="snippet", mine=True,
                                                     pageToken=subscriptions["nextPageToken"],
                                                     maxResults=50).execute()
        for item in subscriptions["items"]:
            if item not in result:
                result.append(item)
    return result


def retrieve_all_subscription_channel_ids(youtube=None) -> Set[str]:
    subscriptions = retrieve_all_subscriptions(youtube)
    return {subscription["snippet"]["resourceId"]["channelId"] for subscription in subscriptions}


def subscribe(channel_ids: Set[str], youtube=None):
    if youtube is None:
        flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes_youtube)
        credentials = flow.run_local_server(port=8082)
        youtube = build("youtube", "v3", credentials=credentials)
    subscribed_ids = retrieve_all_subscription_channel_ids(youtube)
    for channel_id in channel_ids:
        if channel_id not in subscribed_ids:
            sleep(.2)
            youtube.subscriptions().insert(part='snippet',
                                           body={"snippet": {"resourceId": {"channelId": channel_id}}}).execute()


def unsubscribe_all(youtube=None):
    if youtube is None:
        flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes_youtube)
        credentials = flow.run_local_server(port=8083)
        youtube = build("youtube", "v3", credentials=credentials)
    subscriptions = retrieve_all_subscriptions(youtube)
    for subscription in subscriptions:
        youtube.subscriptions().delete(id=subscription["id"]).execute()


if __name__ == '__main__':
    ids = retrieve_all_subscription_channel_ids()
    subscribe(ids)
