import json
import requests
from bs4 import BeautifulSoup as BSoup
import sys

# Colors for printing (assuming FONT is some color class, if it's not you can define it yourself)
class FONT:
    GREEN = '\x1b[32m'
    CYAN = '\x1b[36m'
    RED = '\x1b[31m'
    RESET = '\x1b[0m'
    BOLD = '\x1b[1m'

ESC = '\x1b'
RED = ESC + '[31m'
GREEN = ESC + '[32m'

TIKTOK_URL = 'https://www.tiktok.com/@'  # URL format for TikTok usernames
TELCODE = '@example_username'  # Replace with the target TikTok username

def get_tiktoker_data(username: str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/114.0.5748.222 Safari/537.36'
    }

    print("\n\n" + FONT.GREEN + "[" + FONT.CYAN + "<>" + FONT.RESET + FONT.GREEN + "]" + FONT.CYAN + " Результаты поиска по ТикТок аккаунту:")

    try:
        response = requests.get(TIKTOK_URL + username, headers=headers, timeout=10)
        response.raise_for_status()  # Check for request errors

        soup = BSoup(response.text, 'html.parser')
        script_tag = soup.find('script', id='__UNIVERSAL_DATA_FOR_REHYDRATION__', type='application/json')

        if script_tag:
            try:
                json_data = json.loads(script_tag.string)
                user_data = json_data.get('__DEFAULT_SCOPE__', {}).get('webapp.user-detail', {})
                
                if user_data:
                    user_info = user_data.get("userInfo", {})
                    user_stats = user_info.get("stats", {})

                    account_id = user_info.get("user", {}).get("id", "Неизвестно")
                    unique_id = user_info.get("user", {}).get("uniqueId", "Неизвестно")
                    nickname = user_info.get("user", {}).get("nickname", "Неизвестно")
                    bios = user_info.get("user", {}).get("signature", "Неизвестно")
                    private_account = user_info.get("user", {}).get("privateAccount", "Неизвестно")
                    user_country = user_info.get("user", {}).get("region", "Неизвестно")
                    account_language = user_info.get("user", {}).get("language", "Неизвестно")
                    follower_count = user_stats.get("followerCount", "Неизвестно")
                    following_count = user_stats.get("followingCount", "Неизвестно")
                    heart_count = user_stats.get("heartCount", "Неизвестно")
                    video_count = user_stats.get("videoCount", "Неизвестно")

                    print('\n' + '-' * 15 + f' User Information ' + '-' * 15)
                    print(f"ID аккаунта: {account_id}")
                    print(f"Уникальный ID: {unique_id}")
                    print(f"Никнейм: {nickname}")
                    print(f"Описание: {bios}")
                    print(f"Закрытый аккаунт: {private_account}")
                    print(f"Страна: {user_country}")
                    print(f"Язык аккаунта: {account_language}")
                    print(f"\nКол-во подписчиков: {follower_count}")
                    print(f"Кол-во подписок: {following_count}")
                    print(f"Кол-во лайков: {heart_count}")
                    print(f"Кол-во видео: {video_count}")
                else:
                    print(FONT.RED + "Нет данных пользователя" + FONT.RESET)

            except json.JSONDecodeError:
                print(FONT.RED + "Ошибка декодирования JSON." + FONT.RESET)
                sys.exit()
            except KeyError as e:
                print(FONT.RED + f"Ключ не найден в JSON: {e}" + FONT.RESET)
                sys.exit()
        else:
            print(FONT.RED + "Тег <script> не найден" + FONT.RESET)
            sys.exit()

    except requests.exceptions.RequestException as e:
        print(FONT.RED + FONT.BOLD + f"Ошибка соединения: {e}. Нет подключения к интернету" + FONT.RESET)
        sys.exit()

def main():
    username = TELCODE.lstrip('@')  # Remove @ if it's present
    get_tiktoker_data(username)

if __name__ == '__main__':
    main()
