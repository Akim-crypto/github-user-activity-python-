import sys 
import json
import urllib.request
import urllib.error

def fetch_github_activity(username):
    url = f"https://api.github.com/users/{username}/events"
    try:
        with urllib.request.urlopen(url) as response:
            if response.status != 200 :
                print(f"Ошибка : статус {response.status}")
                return
            data = response.read()
            events = json.loads(data)
            if not events:
                print("нет недавней активности для пользователя")
                return
            for event in events:
                print(format_event(event))
    except urllib.error.HTTPError as e :
        if e.code == 404 :
            print("Ошибка: пользователь не найден")
        else :
            print(f"Ошибка HTTP {e.code}")
    except Exception as e :
        print(f"Не удалось получить данные: {e}")


def format_event(event):
    event_type = event.get("type" , "UnknownEvent")
    repo_name = event.get("repo" , {}).get("name" , "unknown/repo")
    if event_type == "PushEvent":
        commits = len(event.get("payload" , {}).get("commits",[]))
        return f"Pushed {commits} commits to {repo_name}"
    elif event_type == "IssueEvent":
        action = event.get("payload",{}).get("action","unknown")
        return f"{action.capitalize()} an issue in {repo_name}"
    elif event_type == "WatchEvent":
        return f"Starred {repo_name}"
    else:
        return f"{event_type} in {repo_name}"
    

def main():
    username = input("Введите имя пользователя Github: ").strip()
    if not username:
        print("имя пользователя не указано.")
        return
    fetch_github_activity(username)

if __name__ == "__main__":
    main() 



