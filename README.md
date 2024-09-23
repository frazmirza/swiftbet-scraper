<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>

<h1>Swiftbet Scraper</h1>

<h2>Introduction</h2>
<p>This project automates the process of scraping data from the Swiftbet website, focusing on horse racing information from Australia (AU) and New Zealand (NZ). The initial stage involves extracting detailed race records, which are systematically stored in CSV files. A secondary bot, built using Selenium, randomly selects race URLs from the CSV file and scrapes the prices of horses participating in those races and store into CSV file.

The project employs a robust stack of technologies, including Python, Selenium, Beautiful Soup, and Celery, to efficiently handle web scraping and automation tasks. The codebase adheres to industry-standard practices for Python development, maintaining high-quality code through automated checks for linting and formatting using flake8 and isort..</p>

<h2>How to Install</h2>
<ol>
    <li>Clone the repository:</li>
    <pre><code>git clone https://github.com/frazmirza/swiftbet-scraper.git
cd swiftbet-scraper
    </code></pre>
  <li>Set up a virtual environment:</li>
        <pre><code>python -m venv venv </code></pre>
  <li><pre><code>source venv/bin/activate   # On Windows: venv\Scripts\activate </code></pre>
  </li>

  <li>Install the required dependencies:
        <pre><code>pip install -r requirements.txt</code></pre>
  </li>
</ol>

<h2>Run the Project with multiple Ways</h2>
<ol>
    <li>Make Sure you install requirements.txt:
        <ul>
        <li>For Bash(To run Redis + Celery + Celery Beat Automatically) : script will run automatically run after 2 minutes:
            <pre><code>
./start-celery-beat.sh
            </code></pre>
        </li>
            <li>OR Excecute below commands in separate terminal: script will run automatically run after 2 minutes:
                <pre><code>redis-server</code></pre>
                <pre><code>celery -A celery_app worker --loglevel=info</code></pre>
                <pre><code>celery -A celery_app beat --loglevel=info</code></pre>
            </li>
        </ul>
    </li>
    <li>Run without Celery Worker:
        <ul>
        <li>Excecute main.py file in terminal:
            <pre><code>
python main.py
            </code></pre>
    </li>

    
</ol>

<h2>GitHub Actions for Code Formatting</h2>
<p>We have included <strong>GitHub Actions</strong> to automatically check the code formatting and style using <code>flake8</code> and <code>isort</code>.</p>

<h3>GitHub Action for Linting</h3>

<pre><code>
name: Linting

on:
  push:
    branches:
      - main
  pull_request:

jobs:
  lint:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install flake8 isort

    - name: Run isort
      run: |
        isort --recursive .

    - name: Run Flake8
      run: |
        flake8 .
</code></pre>

<p>This workflow will automatically check your code for proper formatting each time you push or create a pull request. The checks include:</p>
<ul>
    <li><strong>flake8</strong>: For linting and ensuring adherence to Python coding standards.</li>
    <li><strong>isort</strong>: For sorting and organizing imports according to PEP8.</li>
</ul>

<h2>Addition Information</h2>
<p>You can make your requests anonymous by uncommenting the relevant code in the Bot.py file, which alters the IP address and User-Agent during execution.</p>
<pre><code>
  # Add a random User-Agent
  ua = UserAgent()
  user_agent = ua.random  # Generate a random User-Agent
  self.options.add_argument(f"user-agent={user_agent}")
  # Fake IP address (using a proxy server for this purpose)
  # Replace this with an actual proxy IP address
  # or a dynamic method to get proxy IPs
  fake_ip = "YUR IP Add"
  self.options.add_argument(f"--proxy-server={fake_ip}")
  
</code></pre>


<h2>Author</h2>
<blockquote>
  Fraz Ahmad<br>
  Email: frazmirza58@gmail.com
</blockquote>

<div align="center">
    <h3>========Thank You !!!=========</h3>
</div>
</body>
</html>
