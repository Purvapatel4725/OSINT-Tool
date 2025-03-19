# OSINT-Tool: Enhanced Open Source Intelligence Search Tool

A comprehensive command-line tool for gathering information about individuals from public sources. This tool is designed to assist with legitimate privacy removal services, personal data management, and information gathering from publicly available sources.

⚠️ **IMPORTANT LEGAL DISCLAIMER** ⚠️
> This tool is provided for educational and ethical use only. Using this tool to collect information without consent may violate privacy laws in your jurisdiction. The author (Purva Patel) is not responsible for any misuse or illegal activities conducted with this tool. Users are solely responsible for complying with applicable laws and regulations in their jurisdiction. Using this tool for harassment, stalking, or any malicious purpose is strictly prohibited.

## Features

- **Interactive Mode**: Easy-to-use interactive interface for data collection
- **Command Line Arguments**: Flexible automation through command-line options
- **Comprehensive Search**: Searches across multiple platforms including:
  - Social media platforms
  - People directories
  - Public records
  - Professional networks
  - Email and phone lookups
  - Username searches
  - Employment and education records
  - Family/relative connections
  - Reverse image search
- **Advanced Search Techniques**:
  - Google dorking for targeted results
  - Web archive searches
  - Data breach indicators
  - Professional network analysis
- **Export Options**: Save results in JSON or TXT format
- **Browser Integration**: Open search results directly in your web browser

## Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Purvapatel4725/OSINT-Tool.git
cd OSINT-Tool
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:
  - On Windows:

   ```bash
   venv\Scripts\activate
   ```
   - On macOS/Linux:

   ```bash
   source venv/bin/activate
   ```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Interactive Mode

Run the tool in interactive mode where you'll be prompted for all required information:

```bash
python osinttool.py --interactive
```

or simply:

```bash
python osinttool.py
```

### Command-Line Arguments

For scripting or automation, use command-line arguments:

```bash
python testfile2.py --name "John Doe" --email "john@example.com" --phone "555-123-4567"
```

### Basic Options

```
-i, --interactive     Run in interactive mode
-n, --name            Subject's full name (required in non-interactive mode)
-b, --birth           Birth date (YYYY-MM-DD)
-a, --address         Address (can be used multiple times)
-e, --email           Email address (can be used multiple times)
-p, --phone           Phone number (can be used multiple times)
-u, --username        Username (can be used multiple times)
--employer            Employer (can be used multiple times)
--education           Educational institution (can be used multiple times)
--relative            Relative (can be used multiple times)
--photo               Path to photo for reverse image search
```

### Output Options

```
-o, --output          Output file name (without extension)
-f, --format          Output format (json or txt, default: json)
--browser             Open results in browser
```

### Advanced Search Options

```
-d, --dorking         Enable advanced Google dorking
--archives            Search web archives
--breaches            Check for data breach indicators
--professional        Search professional networks
--all                 Enable all advanced search features
```

### Example Commands

Basic search with name only:
```bash
python osinttool.py --name "John Smith"
```

Comprehensive search with multiple data points:
```bash
python osinttool.py --name "John Smith" --email "john.smith@example.com" --phone "555-123-4567" --username "jsmith" --employer "ACME Corporation" --all
```

Custom output file in text format:
```bash
python osinttool.py --name "John Smith" --output "smith_results" --format txt
```

## Understanding the Results

The tool generates two types of outputs:

1. **Console Output**: Summary information displayed in the terminal
2. **File Output**: Detailed results saved in either JSON or TXT format

The results include:

- **Subject Information**: All provided information about the subject
- **Search Results**: Categorized by search type (Social Media, People Directories, etc.)
- **Metadata**: Timestamp, search count, and other information

### Results Structure

The JSON output is structured as follows:

```json
{
  "subject_info": {
    "name": "Subject Name",
    "emails": ["email@example.com"],
    ...
  },
  "search_results": {
    "Search Type 1": {
      "url": "https://example.com/search",
      "category": "Category",
      "info": "Description"
    },
    ...
  },
  "metadata": {
    "timestamp": "2023-03-18 12:34:56",
    "search_count": 42
  }
}
```

## Best Practices

1. **Start Broad**: Begin with basic information and narrow your search
2. **Verify Information**: Cross-reference findings across multiple sources
3. **Be Patient**: OSINT research is often time-consuming and requires persistence
4. **Document Everything**: Save all findings, including seemingly minor details
5. **Respect Privacy**: Always consider ethical implications of information gathering

## Contributing

Contributions are welcome! This is an open-source project, and we encourage improvements.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please make sure your code follows the project's style guidelines and includes appropriate documentation.

## Author

Purva Patel

---

Remember: Use this tool responsibly and ethically. Always respect privacy and adhere to all applicable laws.
