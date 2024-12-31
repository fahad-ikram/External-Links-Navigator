import streamlit as st
import requests
import time
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urlparse
# Function to extract the domain from a URL
def extract_domain(url):
    try:
        parsed = urlparse(url)
        return parsed.netloc.split(':')[0]
    except Exception as e:
        st.error(f"Error extracting domain: {e}")
        return None
# List of social media domains to exclude
SOCIAL_MEDIA_DOMAINS = [
    "facebook.com", "twitter.com", "instagram.com", "linkedin.com",
    "youtube.com", "x.com", "tiktok.com", "pinterest.com",
    "flipboard.com", "google", "#"
]
# Function to validate a URL
def is_valid_url(url):
    try:
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)
    except Exception:
        return False
# Function to filter links
def filter_links(hrefs, base_url, social_media_domains):
    return [
        link for link in hrefs
        if is_valid_url(link)  # Check if the URL is valid
        and base_url not in link  # Exclude internal links
        and not any(domain in link for domain in social_media_domains)  # Exclude social media links
    ]
# Streamlit user inputs
st.title("External Links Navigator")
url = st.text_input("Enter the URL", key="url")
article_class = st.text_input("Enter the CSS class name of article", key="article_class")
progress_bar = st.progress(0)
status_text = st.empty()
if url and article_class:
    if not is_valid_url(url):
        st.error("Please enter a valid URL.")
    else:
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, features="html.parser")
            # Extract article links
            article_links = soup.find_all(class_=article_class)
            # Find all 'a' tags within each article link
            article_hrefs = []
            for article_link in article_links:
                article_hrefs.append(article_link.find('a'))
            # Get the href attribute from each 'a' tag
            hrefs = [a.get('href') for a in article_hrefs if a.get('href') is not None]
            external_links = []
            for i, href in enumerate(hrefs, start=1):
                try:
                    article_response = requests.get(href)
                    article_soup = BeautifulSoup(article_response.content, features="html.parser")
                    all_links = article_soup.find_all('a')
                    hrefs_in_article = [a.get('href') for a in all_links if a.get('href')]
                    # Filter and collect external links
                    filtered_links = filter_links(hrefs_in_article, extract_domain(url), SOCIAL_MEDIA_DOMAINS)
                    external_links.extend(filtered_links)
                    # Update progress bar and status
                    status_text.text(f"Processing article {i}/{len(hrefs)}")
                    progress_bar.progress(i / len(hrefs))
                    time.sleep(2)
                except requests.exceptions.RequestException as e:
                    st.warning(f"Error fetching {href}: {e}")
            # Extract unique domains
            unique_domains = {extract_domain(link) for link in external_links}
            unique_domains.discard(None)  # Remove None values
            st.write(f'Total External links :  {len(unique_domains)}')
            # Convert the external links to a CSV
            if unique_domains:
                df = pd.DataFrame(sorted(unique_domains), columns=["External Links"])
                csv_data = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv_data,
                    file_name="external_links.csv",
                    mime="text/csv"
                )
            # Display results
            st.subheader("Extracted External Links")
            for domain in sorted(unique_domains):
                st.write(f"https://{domain}/")
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching URL: {e}")