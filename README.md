# External Links Navigator

This Streamlit app extracts external links from a specific article section of a webpage, filters out social media and internal links, and displays the unique domains of the external links.

## Features

- Accepts a URL and a CSS class name to identify the article section.
- Extracts all links from the specified section of the webpage.
- Filters out:
  - Internal links.
  - Social media links (e.g., Facebook, Twitter).
- Displays unique external domains.
- Provides real-time progress updates during link extraction.

## How It Works

1. **Input the URL and CSS Class Name:**
   - The app takes a URL of a webpage and the CSS class name of the article section.
2. **Webpage Scraping:**
   - Uses the `requests` library to fetch the webpage and `BeautifulSoup` for parsing HTML.
3. **Link Extraction:**
   - Finds all `<a>` tags within the specified article section and extracts their `href` attributes.
4. **Link Filtering:**
   - Filters out invalid links, internal links, and links from social media platforms.
5. **Display Results:**
   - Shows a list of unique external domains extracted from the links.

## Installation

1. Clone this repository or copy the script.
2. Install the required libraries:

   ```bash
   pip install streamlit requests beautifulsoup4
   ```

3. Run the app:

   ```bash
   streamlit run app.py
   ```

## Usage

1. Open the Streamlit app in your browser.
2. Enter the following inputs:
   - **URL:** The webpage URL to scrape.
   - **Article Class Name:** The CSS class name of the section containing the articles.
3. View the extracted external domains in the results section.

## Code Overview

### Key Functions

- `extract_domain(url)`: Extracts the domain from a given URL.
- `is_valid_url(url)`: Validates if the provided URL is properly formatted.
- `filter_links(hrefs, base_url, social_media_domains)`: Filters out internal and social media links from a list of URLs.

### Workflow

1. The app validates the provided URL.
2. Scrapes the specified section of the webpage using `BeautifulSoup`.
3. Extracts all hyperlinks within the section.
4. Iterates through each hyperlink to fetch its content and extract further links.
5. Filters and collects unique external domains.
6. Displays the results in the app.

### Excluded Domains

The app excludes the following social media domains:

- `facebook.com`
- `twitter.com`
- `instagram.com`
- `linkedin.com`
- `youtube.com`
- `x.com`
- `tiktok.com`
- `pinterest.com`
- `flipboard.com`
- Any URL containing `google` or Starts with `#`.

## Example

1. Input the URL `https://example.com/articles`.
2. Specify the article class name as `article-content`.
3. The app processes the links, filters them, and displays unique external domains such as:

   ```\
   https://externaldomain1.com/
   https://externaldomain2.com/
   ```

## Error Handling

- Displays an error if the URL is invalid.
- Warns the user if there's an issue fetching a specific link.

## Limitations

- Requires the CSS class name of the article section to be known.
- Relies on the structure of the webpage for accurate link extraction.

## External Links Download

This code snippet demonstrates how to generate and download a CSV file containing the total count and a list of all unique external links found on a webpage.

**Key Functionality:**

- **Checks for external links:** Verifies if the `unique_domains` variable, assumed to be a collection of unique external link domains, contains any elements.
- **Creates a pandas DataFrame:** If `unique_domains` is not empty, constructs a pandas DataFrame with a single column named "External Links" to hold the sorted list of unique domains.

- **Converts to CSV:** Transforms the DataFrame into a CSV string using `df.to_csv(index=False)` and stores it in the `csv_data` variable.

- **Generates Download Button:** Utilizes `st.download_button` from the Streamlit library to create a downloadable button labeled "Download CSV." Clicking this button initiates the download of the CSV file.
