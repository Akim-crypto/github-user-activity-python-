import requests

# def fetch_github_activity(username):
#     url = f"https://api.github.com/users/{username}/events"
#     try:
#         response = requests.get(url)
#         if response.status_code == 404:
#             print("Ошибка: пользователь не найден")
#             return
#         elif response.status_code != 200:
#             print(f"Ошибка статус: {response.status_code}")
#             return
        
#         events = response.json()
#         if not events:
#             print("Нет недавней активности")
#             return
        
#         for event in events:
#             print(format_event(event))
#     except requests.RequestException as e :
#         print(f"Не удалось получить данные: {e}")


def fetch_github_activity(username):
    url = f"https://api.github.com/users/{username}/events"
    try:
        response = requests.get(url)
        if response.status_code == 404:
            return "Ошибка: пользователь не найден"
        elif response.status_code != 200:
            return f"Ошибка статус: {response.status_code}"

        events = response.json()
        if not events:
            return "Нет недавней активности"

        results = [format_event(event) for event in events]
        return results
    except requests.RequestException as e:
        return f"Не удалось получить данные: {e}"

        
    

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
    

# def main():
#     username = input("Введите имя пользователя Github: ").strip()
#     if not username:
#         print("имя пользователя не указано.")
#         return
#     fetch_github_activity(username)

# if __name__ == "__main__":
#     main() 



