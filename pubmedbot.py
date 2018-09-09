import os, time, re

from slackclient import SlackClient
from pubmed import *

slack_client = SlackClient('slackbotid')# Add Slack bot id



def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """

    response = None
    # This is where you start to implement more commands!
    # if command.startswith(EXAMPLE_COMMAND):
    results = search()
    id_list = results["IdList"]
    response = ""
    if len(id_list):
        papers = fetch_details(id_list)
        for paper in papers:
            response += "*%s*\n_%s_\nhttps://www.ncbi.nlm.nih.gov/pubmed/?term=%s\n\n\n\n" %(paper['MedlineCitation']['Article']['ArticleTitle'],
                                                                                     paper["MedlineCitation"]["Article"]["Abstract"]["AbstractText"][0],
                                                                                     paper["MedlineCitation"]["PMID"]
                                                                                                                         )
    else:
        response = ""

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or None
    )

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            # print(command, channel)
            # if command:
            command = "Anmol You are Idiot"
            handle_command(command, "channel_id")# Add channel id
            time.sleep(period*24*3600)
    else:
        print("Connection failed. Exception traceback printed above.")
