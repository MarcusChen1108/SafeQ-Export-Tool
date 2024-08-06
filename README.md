# safeQ_exporter
export safeq server user data to csv.
# SafeQ Export Tool

SafeQ Export Tool is a Python-based utility designed to export user data from multiple SafeQ servers simultaneously. It provides an easy-to-use interface for system administrators to automate the process of exporting user information from various SafeQ installations.

![SafeQ Export Tool Banner](https://via.placeholder.com/800x200?text=SafeQ+Export+Tool)

## Features

- Export user data from multiple SafeQ servers in one go
- Configurable server settings through an INI file
- Automated login and CSRF token handling
- Export results saved as CSV files with timestamps
- Detailed logging for troubleshooting
- Cross-platform compatibility (Windows, macOS, Linux)

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

## Installation

1. Clone this repository or download the source code:
   ```
   git clone https://github.com/yourusername/safeq-export-tool.git
   cd safeq-export-tool
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration

1. Run the script once to generate a template configuration file:
   ```
   python main.py
   ```

2. Edit the generated `config.ini` file with your SafeQ server details:
   ```ini
   [Server1]
   BASE_URL = http://server1.example.com
   USERNAME = admin1
   PASSWORD = password1
   FILEPATH = ./downloads1

   [Server2]
   BASE_URL = http://server2.example.com
   USERNAME = admin2
   PASSWORD = password2
   FILEPATH = ./downloads2
   ```

   Add as many server sections as needed.

## Usage

Run the script with the following command:

```
python main.py
```

Optional arguments:
- `-c` or `--config`: Specify a custom configuration file path

Example:
```
python main.py -c /path/to/custom/config.ini
```

## Building Executable

To create a standalone executable, you can use PyInstaller:

```
pyinstaller -F -c -i .\safeQ.ico -n safeq_exporter .\main.py
```

This will generate a `safeq_exporter.exe` file in the `dist` directory.

## Troubleshooting

- If you encounter connection issues, ensure that the SafeQ servers are accessible from your network.
- Check the log output for detailed error messages and connection status.
- Verify that the credentials in the `config.ini` file are correct and have the necessary permissions to export user data.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is not officially associated with or endorsed by YSoft SafeQ. Use at your own risk and ensure you have the necessary permissions to export user data from your SafeQ installations.

## Support

If you encounter any issues or have questions, please [open an issue](https://github.com/yourusername/safeq-export-tool/issues) on GitHub.
