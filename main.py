# pyinstaller -F -c -i .\safeQ.ico -n safeq_exporter .\main.py
import requests
import uuid
from bs4 import BeautifulSoup
import logging
import datetime
import os
import sys
import argparse
import configparser
import time

# Configuration file path
DEFAULT_CONFIG_FILE = os.path.dirname(os.path.abspath(__file__)) + "/config.ini"


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def load_config(config_file):
    """Load configuration from file."""
    if not os.path.exists(config_file):
        logging.error(f"Config file {config_file} not found.")
        create_config_file(config_file)
        sys.exit(1)

    config = configparser.ConfigParser()
    config.read(config_file)

    # Check for missing parameters
    required_params = ["BASE_URL", "USERNAME", "PASSWORD", "FILEPATH"]
    for section in config.sections():
        missing_params = [
            param for param in required_params if param not in config[section]
        ]
        if missing_params:
            logging.error(
                f"Missing parameters in section {section}: {', '.join(missing_params)}"
            )
            input(
                f"\n!!! Please edit the config file [ {config_file} ] to include all required parameters.\n"
            )
            sys.exit(1)

    return config


def create_config_file(config_file):
    """Create a template configuration file."""
    config = configparser.ConfigParser()

    for i in range(1, 4):
        section = f"Server{i}"
        config[section] = {
            "BASE_URL": f"http://server{i}.example.com",
            "USERNAME": f"admin{i}",
            "PASSWORD": f"password{i}",
            "FILEPATH": f"./downloads{i}",
        }

    try:
        with open(config_file, "w") as f:
            config.write(f)
        input(
            f"!!! Config file [ {config_file} ] has been created. Please edit it with your actual settings."
        )
    except IOError as e:
        logging.error(f"Failed to create config file. Error: {str(e)}")


class UserExporter:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.csrf_token = None
        self.timeout = 10  # Set a default timeout of 10 seconds

    def login(self, username, password):
        login_url = f"{self.base_url}/login"
        self.csrf_token = str(uuid.uuid4())

        login_data = {
            "username": username,
            "password": password,
            "_csrf": self.csrf_token,
        }

        try:
            response = self.session.post(
                login_url, data=login_data, timeout=self.timeout
            )
            response.raise_for_status()  # Raise an exception for bad status codes

            logging.info("Login successful")
            jsessionid = self.session.cookies.get("JSESSIONID")
            logging.info(f"JSESSIONID: {jsessionid}")
            self.update_csrf_token()
            return True
        except requests.Timeout:
            logging.error(f"Login request timed out after {self.timeout} seconds")
        except requests.ConnectionError:
            logging.error(
                "Failed to connect to the server. Please check your internet connection and the server status."
            )
        except requests.RequestException as e:
            logging.error(f"Login failed. Error: {str(e)}")
        return False

    def update_csrf_token(self):
        try:
            response = self.session.get(
                f"{self.base_url}/web/Dashboard", timeout=self.timeout
            )
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            self.csrf_token = soup.find("meta", {"name": "_csrf"})["content"]
            logging.info(f"Updated CSRF Token: {self.csrf_token}")
        except requests.Timeout:
            logging.error(
                f"CSRF token update request timed out after {self.timeout} seconds"
            )
        except requests.RequestException as e:
            logging.error(f"Failed to update CSRF token. Error: {str(e)}")

    def export_users(self, filepath, section):
        export_url = f"{self.base_url}/servlet/users.ExportUsersServlet"

        export_data = {
            "redirect": "/WEB-INF/views/legacy/web/UserList.jsp",
            "charset": "UTF8",
            "users": "1",
            "_csrf": self.csrf_token,
        }

        try:
            response = self.session.post(
                export_url, data=export_data, timeout=self.timeout
            )
            response.raise_for_status()

            filename = f"{section}_exported_users_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            full_path = os.path.join(filepath, filename)
            self.save_file(full_path, response.content)
            logging.info(f"File '{filename}' has been saved to {full_path}.")
            return True
        except requests.Timeout:
            logging.error(f"Export request timed out after {self.timeout} seconds")
        except requests.RequestException as e:
            logging.error(f"Failed to export users. Error: {str(e)}")
        return False

    @staticmethod
    def save_file(filename, content):
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "wb") as file:
                file.write(content)
        except IOError as e:
            logging.error(f"Failed to save file. Error: {str(e)}")


def main():
    print(
        """

 ░▒▓███████▓▒░░▒▓██████▓▒░░▒▓████████▓▒░▒▓████████▓▒░▒▓██████▓▒░  
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░ 
 ░▒▓██████▓▒░░▒▓████████▓▒░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░ 
       ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░ 
       ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓████████▓▒░▒▓██████▓▒░  
                                                       ░▒▓█▓▒░     
SafeQ Export Tool                        Ver.2024.08.06 ░▒▓█▓▒░   
-----------------------------------------------------------------
                                               
Usage: safeq_exporter.exe [-h] [-c CONFIG]

"""
    )
    parser = argparse.ArgumentParser(description="Export users from multiple servers.")
    parser.add_argument(
        "-c",
        "--config",
        default=DEFAULT_CONFIG_FILE,
        help="Path to the configuration file",
    )
    args = parser.parse_args()

    config = load_config(args.config)

    for section in config.sections():
        logging.info(f"Processing server: {section}")
        base_url = config[section]["BASE_URL"]
        username = config[section]["USERNAME"]
        password = config[section]["PASSWORD"]
        filepath = config[section]["FILEPATH"]

        exporter = UserExporter(base_url)
        if exporter.login(username, password):
            exporter.export_users(filepath, section)
        else:
            logging.error(f"Failed to process server {section}")

    # 倒计时 退出程序
    for i in range(10, 0, -1):
        print("\rThis App will terminate in {} seconds.".format(i), end="", flush=True)
        time.sleep(1)
    print("\rBye-bye!                                 ")


if __name__ == "__main__":
    main()
