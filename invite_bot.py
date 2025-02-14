import requests
import time
import json
import os 


def goodUsers(users, min_level):
    # Filter users based on min_level and find the highest level user.
    invited_users = []
    max_level = 0
    max_level_user = None

    for user in users:
        if user["stats"]["lvl"] >= min_level:
            invited_users.append(user["_id"])
        if user["stats"]["lvl"] > max_level:
            max_level = user["stats"]["lvl"]
            max_level_user = user

    return invited_users, max_level_user


def inviteUser(userId, groupId, headers):
    # Invite a user to the group.
    inviteURL = f'https://habitica.com/api/v3/groups/{groupId}/invite'
    payload = {'uuids': [userId]}
    response = requests.post(inviteURL, json=payload, headers=headers)

    if response.status_code == 200:
        print(f"User {userId} invited successfully.")
    else:
        print(f"Failed to invite user {userId}. Error: {response.text}")


def create_default_config(config_file):
    # Create a default config file.
    default_config = {
        "userAPI": "your-user-api-key",
        "tokenAPI": "your-token-api-key",
        "groupId": "your-group-id",
        "delay": 60,
        "min_level": 10
    }
    with open(config_file, 'w') as file:
        json.dump(default_config, file, indent=4)
    print(f"Default config file created: {config_file}")
    print("Please update the file with your actual configuration.")


def load_config(config_file):
    # Load config from JSON file.
    if not os.path.exists(config_file):
        create_default_config(config_file)
        raise SystemExit("Please update the config file and restart the script.")

    with open(config_file, 'r') as file:
        config = json.load(file)
    
    # Check if the config is valid.
    required_keys = ["userAPI", "tokenAPI", "groupId", "delay", "min_level"]
    if any(config.get(key) in [None, "", f"your-{key.lower()}"] for key in required_keys):
        print("Config file contains placeholder values. Please update it.")
        raise SystemExit("Update the config file and restart the script.")

    return config


def main():
    # Main function to run the Habitica invite bot.
    config_file = 'config.json'
    config = load_config(config_file)

    userAPI = config['userAPI']
    tokenAPI = config['tokenAPI']
    groupId = config['groupId']
    delay = config['delay']
    min_level = config['min_level']
    sessionAmount = 1

    headers = {
        'x-api-user': userAPI,
        'x-api-key': tokenAPI,
    }

    while True:
        print("―――――")
        print(f"Session: {time.time()} | {sessionAmount}")
        sessionAmount += 1
        print()

        userRequest = requests.get('https://habitica.com/api/v3/user', headers=headers)
        print("Got user data!")
        userData = userRequest.json()
        partyId = userData['data']['party']['_id']
        print(f"Party ID: {partyId}")

        partyUserURL = 'https://habitica.com/api/v3/looking-for-party'
        lookingParty = requests.get(partyUserURL, headers=headers)
        print("Got people looking for party!")
        print(f"Users looking for party: {len(lookingParty.json()['data'])}")

        usersList, max_level_user = goodUsers(lookingParty.json()["data"], min_level)
        print(f"Users to invite: {len(usersList)}")

        if max_level_user:
            print(f"Best user: {max_level_user['profile']['name']} (Level: {max_level_user['stats']['lvl']})")
        else:
            print("There is no best user.")
        
        print()

        if len(usersList) == 0:
            print(f"No users to invite. Waiting {delay} seconds...")
            time.sleep(delay)
            continue

        for userId in usersList:
            inviteUser(userId, partyId, headers)

        print()
        print(f"Waiting {delay} seconds...")
        time.sleep(delay)


if __name__ == "__main__":
    main()
