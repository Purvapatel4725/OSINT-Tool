import requests
import re
import webbrowser
import time
import json
import os
import argparse
import sys
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import quote_plus, urlparse

class EnhancedOSINTSearcher:
    def __init__(self):
        self.results = {
            "subject_info": {},
            "search_results": {},
            "metadata": {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "search_count": 0
            }
        }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
        }
        self.output_file = None
        
    def interactive_mode(self):
        """Run the tool in interactive mode, gathering input from the user"""
        print("\n" + "=" * 60)
        print("ENHANCED OSINT SEARCH TOOL - INTERACTIVE MODE")
        print("=" * 60)
        print("Enter information about the subject. Press Enter to skip any field.")
        print("For multiple entries (emails, phones, etc.), separate with commas.")
        
        # Get basic information
        self.results["subject_info"]["name"] = input("\nFull Name: ").strip()
        if not self.results["subject_info"]["name"]:
            print("Name is required to proceed.")
            return False
            
        # Get birth information
        birth_date = input("Birth Date (YYYY-MM-DD): ").strip()
        birth_place = input("Birth Place: ").strip()
        if birth_date or birth_place:
            self.results["subject_info"]["birth"] = {}
            if birth_date:
                self.results["subject_info"]["birth"]["date"] = birth_date
            if birth_place:
                self.results["subject_info"]["birth"]["place"] = birth_place
        
        # Get multiple addresses
        addresses = input("Addresses (separate multiple with commas): ").strip()
        if addresses:
            self.results["subject_info"]["addresses"] = [addr.strip() for addr in addresses.split(",")]
        
        # Get multiple phone numbers
        phones = input("Phone Numbers (separate multiple with commas): ").strip()
        if phones:
            self.results["subject_info"]["phones"] = [phone.strip() for phone in phones.split(",")]
        
        # Get multiple emails
        emails = input("Email Addresses (separate multiple with commas): ").strip()
        if emails:
            self.results["subject_info"]["emails"] = [email.strip() for email in emails.split(",")]
        
        # Get usernames
        usernames = input("Known Usernames/Handles (separate multiple with commas): ").strip()
        if usernames:
            self.results["subject_info"]["usernames"] = [username.strip() for username in usernames.split(",")]
        
        # Get employment information
        employers = input("Known Employers (separate multiple with commas): ").strip()
        if employers:
            self.results["subject_info"]["employers"] = [employer.strip() for employer in employers.split(",")]
        
        # Educational information
        education = input("Educational Institutions (separate multiple with commas): ").strip()
        if education:
            self.results["subject_info"]["education"] = [school.strip() for school in education.split(",")]
        
        # Get relatives
        relatives = input("Known Relatives (separate multiple with commas): ").strip()
        if relatives:
            self.results["subject_info"]["relatives"] = [relative.strip() for relative in relatives.split(",")]
        
        # Photo for reverse image search
        photo_path = input("Path to photo for reverse image search (optional): ").strip()
        if photo_path and os.path.exists(photo_path):
            self.results["subject_info"]["photo_path"] = photo_path
        
        # Output file name
        default_filename = f"osint_{self.results['subject_info']['name'].replace(' ', '_').lower()}_{int(time.time())}"
        self.output_file = input(f"Output filename (default: {default_filename}): ").strip()
        if not self.output_file:
            self.output_file = default_filename
        
        # Output format
        output_format = input("Output format (json or txt, default: json): ").strip().lower()
        if output_format not in ["json", "txt"]:
            output_format = "json"
        self.results["metadata"]["output_format"] = output_format
        
        # Browser opening preference
        open_browser = input("Open results in browser? (y/n, default: n): ").strip().lower()
        self.results["metadata"]["open_browser"] = open_browser == "y"
        
        return True
        
    def search_person(self):
        """Main search function that coordinates various search methods"""
        if not self.results["subject_info"].get("name"):
            print("Error: Name is required for the search.")
            return False
            
        print("\n" + "=" * 60)
        print(f"STARTING COMPREHENSIVE OSINT SEARCH FOR: {self.results['subject_info']['name']}")
        print("=" * 60)
        
        # Social media search
        print("\nSearching social media platforms...")
        self.search_social_media()
        
        # People directories
        print("\nSearching people directories and public records...")
        self.search_people_directories()
        
        # Email searches
        if self.results["subject_info"].get("emails"):
            print("\nSearching by email addresses...")
            for email in self.results["subject_info"]["emails"]:
                self.search_by_email(email)
        
        # Phone searches
        if self.results["subject_info"].get("phones"):
            print("\nSearching by phone numbers...")
            for phone in self.results["subject_info"]["phones"]:
                self.search_by_phone(phone)
        
        # Username searches
        if self.results["subject_info"].get("usernames"):
            print("\nSearching by usernames...")
            for username in self.results["subject_info"]["usernames"]:
                self.search_by_username(username)
        
        # Employer searches
        if self.results["subject_info"].get("employers"):
            print("\nSearching by employment information...")
            for employer in self.results["subject_info"]["employers"]:
                self.search_by_employer(employer)
        
        # Education searches
        if self.results["subject_info"].get("education"):
            print("\nSearching by educational information...")
            for school in self.results["subject_info"]["education"]:
                self.search_by_education(school)
        
        # Photo reverse search
        if self.results["subject_info"].get("photo_path"):
            print("\nPerforming reverse image search...")
            self.reverse_image_search()
        
        # Family/relative searches
        if self.results["subject_info"].get("relatives"):
            print("\nSearching for information about relatives...")
            for relative in self.results["subject_info"]["relatives"]:
                self.search_by_relative(relative)
        
        # Update metadata
        self.results["metadata"]["search_count"] = len(self.results["search_results"])
        
        # Save results
        self.save_results()
        
        # Display results
        self.display_results()
        
        # Open results in browser if requested
        if self.results["metadata"].get("open_browser"):
            self.open_results_in_browser()
        
        return True
    
    def search_social_media(self):
        """Search for the person across major social media platforms"""
        name = self.results["subject_info"]["name"]
        
        social_platforms = {
            "Facebook": "https://www.facebook.com/search/top/?q={}",
            "LinkedIn": "https://www.google.com/search?q=site:linkedin.com+{}",
            "Twitter": "https://twitter.com/search?q={}",
            "Instagram": "https://www.google.com/search?q=site:instagram.com+{}",
            "TikTok": "https://www.google.com/search?q=site:tiktok.com+{}",
            "YouTube": "https://www.youtube.com/results?search_query={}",
            "Reddit": "https://www.reddit.com/search/?q={}",
            "Pinterest": "https://www.pinterest.com/search/pins/?q={}"
        }
        
        # Add usernames to search if available
        if self.results["subject_info"].get("usernames"):
            for username in self.results["subject_info"]["usernames"]:
                social_platforms[f"Twitter @{username}"] = f"https://twitter.com/{username}"
                social_platforms[f"Instagram @{username}"] = f"https://www.instagram.com/{username}"
                social_platforms[f"TikTok @{username}"] = f"https://www.tiktok.com/@{username}"
        
        # Perform searches
        for platform, url_template in social_platforms.items():
            search_url = url_template.format(quote_plus(name))
            self.results["search_results"][platform] = {
                "url": search_url,
                "category": "Social Media",
                "info": f"Potential {platform} profile for {name}"
            }
            print(f"✓ Generated {platform} search")
    
    def search_people_directories(self):
        """Search people finder and public records sites"""
        name = self.results["subject_info"]["name"]
        name_formatted = name.replace(" ", "-").lower()
        
        # Basic search term
        search_term = name
        
        # Enhanced search term with birth info
        if self.results["subject_info"].get("birth"):
            birth_info = self.results["subject_info"]["birth"]
            if birth_info.get("date"):
                search_term += f" born {birth_info['date']}"
            if birth_info.get("place"):
                search_term += f" {birth_info['place']}"
        
        # Add location if available
        location_term = ""
        if self.results["subject_info"].get("addresses") and self.results["subject_info"]["addresses"]:
            # Use the first address for location context
            location_term = self.results["subject_info"]["addresses"][0]
        
        # People finder sites
        person_finders = {
            "WhitePages": "https://www.whitepages.com/name/{}",
            "Spokeo": "https://www.spokeo.com/{}",
            "BeenVerified": "https://www.beenverified.com/people/{}/",
            "TruePeopleSearch": "https://www.truepeoplesearch.com/results?name={}",
            "Intelius": "https://www.intelius.com/people-search/{}",
            "PeopleFinders": "https://www.peoplefinders.com/people/{}",
            "Radaris": "https://radaris.com/#!search/{}",
            "MyLife": "https://www.mylife.com/search/?searchFirstName={}&searchLastName={}"
        }
        
        # Split first and last name for services that require it
        name_parts = name.split()
        if len(name_parts) >= 2:
            first_name = name_parts[0]
            last_name = name_parts[-1]
            
            # Update MyLife URL
            person_finders["MyLife"] = person_finders["MyLife"].format(quote_plus(first_name), quote_plus(last_name))
        else:
            # If only one name part, use it for both
            person_finders["MyLife"] = person_finders["MyLife"].format(quote_plus(name), quote_plus(name))
        
        # Add all people finder searches
        for site, url_template in person_finders.items():
            if site != "MyLife":  # MyLife was already formatted
                search_url = url_template.format(quote_plus(name_formatted))
            else:
                search_url = url_template
                
            # Add location to TruePeopleSearch if available
            if site == "TruePeopleSearch" and location_term:
                search_url += f"&citystatezip={quote_plus(location_term)}"
                
            self.results["search_results"][site] = {
                "url": search_url,
                "category": "People Directories",
                "info": f"Potential records on {site}"
            }
            print(f"✓ Generated {site} search")
            
        # Public records searches
        public_records = {
            "Google Public Records": f"https://www.google.com/search?q={quote_plus(search_term)}+public+records",
            "Court Records": f"https://www.google.com/search?q={quote_plus(name)}+court+records",
            "Property Records": f"https://www.google.com/search?q={quote_plus(name)}+property+records",
            "Marriage Records": f"https://www.google.com/search?q={quote_plus(name)}+marriage+records",
            "Obituaries": f"https://www.google.com/search?q={quote_plus(name)}+obituary"
        }
        
        # Add location context to property records if available
        if location_term:
            public_records["Property Records"] = f"https://www.google.com/search?q={quote_plus(name)}+property+records+{quote_plus(location_term)}"
        
        # Add all public records searches
        for search_name, url in public_records.items():
            self.results["search_results"][search_name] = {
                "url": url,
                "category": "Public Records",
                "info": f"{search_name} search for {name}"
            }
            print(f"✓ Generated {search_name}")
    
    def search_by_email(self, email):
        """Search based on email address"""
        email_searches = {
            f"Email Lookup ({email})": f"https://thatsthem.com/email/{quote_plus(email)}",
            f"Have I Been Pwned ({email})": f"https://haveibeenpwned.com/account/{quote_plus(email)}",
            f"Google Email Search ({email})": f"https://www.google.com/search?q={quote_plus(email)}",
            f"Hunter.io ({email})": f"https://hunter.io/email-verifier/{quote_plus(email)}"
        }
        
        # Extract domain for additional searches
        domain = email.split('@')[-1] if '@' in email else None
        if domain:
            email_searches[f"Domain Lookup ({domain})"] = f"https://www.google.com/search?q={quote_plus(domain)}+company+information"
        
        for search_name, url in email_searches.items():
            self.results["search_results"][search_name] = {
                "url": url,
                "category": "Email",
                "info": f"Information linked to email: {email}"
            }
            print(f"✓ Generated {search_name}")
    
    def search_by_phone(self, phone):
        """Search based on phone number"""
        # Format phone number (remove non-digits)
        phone_clean = re.sub(r'\D', '', phone)
        
        phone_searches = {
            f"Truecaller ({phone})": f"https://www.truecaller.com/search/{phone_clean}",
            f"Google Phone Search ({phone})": f"https://www.google.com/search?q={quote_plus(phone)}",
            f"WhitePages Phone ({phone})": f"https://www.whitepages.com/phone/{phone_clean}",
            f"Spokeo Phone ({phone})": f"https://www.spokeo.com/phone/{phone_clean}"
        }
        
        for search_name, url in phone_searches.items():
            self.results["search_results"][search_name] = {
                "url": url,
                "category": "Phone",
                "info": f"Information linked to phone: {phone}"
            }
            print(f"✓ Generated {search_name}")
    
    def search_by_username(self, username):
        """Search based on username"""
        username_searches = {
            f"KnowEm ({username})": f"https://knowem.com/checkusernames.php?u={quote_plus(username)}",
            f"NameChk ({username})": f"https://namechk.com/search/{quote_plus(username)}",
            f"GitHub ({username})": f"https://github.com/{quote_plus(username)}",
            f"Twitter ({username})": f"https://twitter.com/{quote_plus(username)}",
            f"Instagram ({username})": f"https://www.instagram.com/{quote_plus(username)}/",
            f"Google Username Search ({username})": f"https://www.google.com/search?q={quote_plus(username)}+profile+OR+account"
        }
        
        for search_name, url in username_searches.items():
            self.results["search_results"][search_name] = {
                "url": url,
                "category": "Username",
                "info": f"Accounts linked to username: {username}"
            }
            print(f"✓ Generated {search_name}")
    
    def search_by_employer(self, employer):
        """Search based on employer information"""
        name = self.results["subject_info"]["name"]
        
        employer_searches = {
            f"{employer} Employee Directory": f"https://www.google.com/search?q={quote_plus(employer)}+employee+directory+{quote_plus(name)}",
            f"{employer} LinkedIn": f"https://www.google.com/search?q=site:linkedin.com+{quote_plus(employer)}+{quote_plus(name)}",
            f"{employer} Contact": f"https://www.google.com/search?q={quote_plus(employer)}+contact+{quote_plus(name)}"
        }
        
        for search_name, url in employer_searches.items():
            self.results["search_results"][search_name] = {
                "url": url,
                "category": "Employment",
                "info": f"Employment information: {name} at {employer}"
            }
            print(f"✓ Generated {search_name}")
    
    def search_by_education(self, school):
        """Search based on educational information"""
        name = self.results["subject_info"]["name"]
        
        education_searches = {
            f"{school} Alumni": f"https://www.google.com/search?q={quote_plus(school)}+alumni+{quote_plus(name)}",
            f"{school} Yearbook": f"https://www.google.com/search?q={quote_plus(school)}+yearbook+{quote_plus(name)}",
            f"{school} Graduation": f"https://www.google.com/search?q={quote_plus(school)}+graduation+{quote_plus(name)}"
        }
        
        for search_name, url in education_searches.items():
            self.results["search_results"][search_name] = {
                "url": url,
                "category": "Education",
                "info": f"Educational information: {name} at {school}"
            }
            print(f"✓ Generated {search_name}")
    
    def search_by_relative(self, relative):
        """Search for information about relatives"""
        name = self.results["subject_info"]["name"]
        
        relative_searches = {
            f"Family Search ({relative})": f"https://www.google.com/search?q={quote_plus(name)}+related+to+{quote_plus(relative)}",
            f"Social Media ({relative})": f"https://www.google.com/search?q={quote_plus(relative)}+social+media+{quote_plus(name)}"
        }
        
        for search_name, url in relative_searches.items():
            self.results["search_results"][search_name] = {
                "url": url,
                "category": "Relatives",
                "info": f"Information about relative: {relative} related to {name}"
            }
            print(f"✓ Generated {search_name}")
    
    def reverse_image_search(self):
        """Generate reverse image search URLs"""
        # We can't actually upload images, but we can provide the URLs for the user
        image_searches = {
            "Google Reverse Image": "https://images.google.com/searchbyimage",
            "TinEye Reverse Image": "https://tineye.com/",
            "Yandex Reverse Image": "https://yandex.com/images/search",
            "Bing Visual Search": "https://www.bing.com/visualsearch"
        }
        
        for search_name, url in image_searches.items():
            self.results["search_results"][search_name] = {
                "url": url,
                "category": "Image Search",
                "info": f"Upload the image at {self.results['subject_info']['photo_path']} to this service"
            }
            print(f"✓ Generated {search_name}")
    
    def display_results(self):
        """Display search results in a readable format"""
        name = self.results["subject_info"]["name"]
        total_results = len(self.results["search_results"])
        
        print("\n" + "=" * 60)
        print(f"OSINT SEARCH RESULTS FOR: {name}")
        print(f"Total Searches Generated: {total_results}")
        print("=" * 60)
        
        # Group results by category
        categories = {}
        for source, data in self.results["search_results"].items():
            category = data["category"]
            if category not in categories:
                categories[category] = []
            categories[category].append((source, data))
        
        # Display results by category
        for category, items in categories.items():
            print(f"\n{category.upper()} ({len(items)} searches)")
            print("-" * 40)
            
            for source, data in items:
                print(f"• {source}")
                print(f"  URL: {data['url']}")
                print(f"  Info: {data['info']}")
                print()
        
        print(f"\nResults saved to: {self.output_file}.{self.results['metadata']['output_format']}")
    
    def save_results(self):
        """Save results to a file"""
        format_type = self.results["metadata"]["output_format"]
        filename = f"{self.output_file}.{format_type}"
        
        try:
            if format_type == "json":
                with open(filename, 'w') as f:
                    json.dump(self.results, f, indent=4)
            else:  # txt format
                with open(filename, 'w') as f:
                    f.write(f"OSINT SEARCH RESULTS FOR: {self.results['subject_info']['name']}\n")
                    f.write(f"Generated on: {self.results['metadata']['timestamp']}\n")
                    f.write(f"Total Searches: {self.results['metadata']['search_count']}\n\n")
                    
                    f.write("SUBJECT INFORMATION\n")
                    f.write("==================\n")
                    for key, value in self.results["subject_info"].items():
                        if key == "photo_path":
                            f.write(f"Photo: {value}\n")
                        else:
                            f.write(f"{key.capitalize()}: {value}\n")
                    
                    f.write("\nSEARCH RESULTS\n")
                    f.write("=============\n")
                    
                    # Group results by category
                    categories = {}
                    for source, data in self.results["search_results"].items():
                        category = data["category"]
                        if category not in categories:
                            categories[category] = []
                        categories[category].append((source, data))
                    
                    # Write results by category
                    for category, items in categories.items():
                        f.write(f"\n{category.upper()} ({len(items)} searches)\n")
                        f.write("-" * 40 + "\n")
                        
                        for source, data in items:
                            f.write(f"• {source}\n")
                            f.write(f"  URL: {data['url']}\n")
                            f.write(f"  Info: {data['info']}\n\n")
            
            print(f"\nResults successfully saved to {filename}")
            
        except Exception as e:
            print(f"Error saving results: {e}")
    
    def open_results_in_browser(self, limit=10):
        """Open search results in web browser"""
        if not self.results["search_results"]:
            print("No results to open.")
            return
            
        print(f"\nOpening up to {limit} results in your default browser...")
        opened = 0
        
        # Ask for confirmation first
        confirm = input(f"This will open up to {limit} browser tabs. Continue? (y/n): ").lower()
        if confirm != "y":
            print("Browser opening cancelled.")
            return
        
        # Open results by category for better organization
        categories = {}
        for source, data in self.results["search_results"].items():
            category = data["category"]
            if category not in categories:
                categories[category] = []
            categories[category].append((source, data))
        
        # Open one from each category first
        for category, items in categories.items():
            if opened >= limit:
                break
                
            source, data = items[0]
            webbrowser.open(data["url"])
            print(f"Opened: {source}")
            opened += 1
            time.sleep(1)  # Delay to prevent overwhelming the browser
        
        # Open remaining results up to the limit
        for category, items in categories.items():
            if opened >= limit:
                break
                
            # Skip the first one since we've already opened it
            for source, data in items[1:]:
                if opened >= limit:
                    break
                    
                webbrowser.open(data["url"])
                print(f"Opened: {source}")
                opened += 1
                time.sleep(1)  # Delay to prevent overwhelming the browser
        
        if opened == limit and len(self.results["search_results"]) > limit:
            print(f"Limit of {limit} results reached. {len(self.results['search_results']) - limit} results not opened.")
            print(f"All results are available in the saved file: {self.output_file}.{self.results['metadata']['output_format']}")


def perform_google_dorking(self, name):
    """Generate advanced Google dork searches for more comprehensive results"""
    print("\nGenerating Google dork searches...")
    
    # Split name into parts for more targeted searches
    name_parts = name.split()
    if len(name_parts) >= 2:
        first_name = name_parts[0]
        last_name = name_parts[-1]
    else:
        first_name = last_name = name
        
    # Encode names for URL
    encoded_name = quote_plus(name)
    encoded_first = quote_plus(first_name)
    encoded_last = quote_plus(last_name)
    
    # Advanced Google dorks for finding personal information
    google_dorks = {
        f"Document Search - {name}": f"https://www.google.com/search?q={encoded_name}+filetype:pdf+OR+filetype:doc+OR+filetype:docx+OR+filetype:xlsx+OR+filetype:pptx",
        f"Contact Information - {name}": f"https://www.google.com/search?q={encoded_name}+\"phone\"+(\"home\"+OR+\"cell\"+OR+\"mobile\")+\"address\"+(\"email\"+OR+\"mail\")",
        f"Social Media Profiles - {name}": f"https://www.google.com/search?q={encoded_name}+intext:\"profile\"+site:facebook.com+OR+site:twitter.com+OR+site:linkedin.com+OR+site:instagram.com",
        f"Forum Posts - {name}": f"https://www.google.com/search?q={encoded_name}+site:reddit.com+OR+site:quora.com+OR+site:stackoverflow.com+OR+site:forums.*",
        f"Personal Information - {name}": f"https://www.google.com/search?q=intitle:\"about\"+intitle:\"me\"+{encoded_name}",
        f"Academic Publications - {name}": f"https://www.google.com/search?q={encoded_name}+site:academia.edu+OR+site:researchgate.net+OR+site:scholar.google.com",
        f"Presentations - {name}": f"https://www.google.com/search?q={encoded_name}+site:slideshare.net+OR+site:prezi.com+OR+filetype:ppt+OR+filetype:pptx",
        f"Public Directories - {name}": f"https://www.google.com/search?q={encoded_name}+inurl:directory+OR+inurl:staff+OR+inurl:employees+OR+inurl:team",
        f"Email Patterns - {name}": f"https://www.google.com/search?q=\"*@*\"+{encoded_first}+{encoded_last}",
        f"News Articles - {name}": f"https://www.google.com/search?q={encoded_name}+site:news.*+OR+site:*.news+OR+site:*.com/news"
    }
    
    # Deeper Google dorks if we have additional information
    if self.results["subject_info"].get("employers"):
        for employer in self.results["subject_info"]["employers"]:
            encoded_employer = quote_plus(employer)
            google_dorks[f"Company Documents - {employer}"] = f"https://www.google.com/search?q=site:{encoded_employer}+intext:{encoded_name}+filetype:pdf+OR+filetype:doc+OR+filetype:docx"
            google_dorks[f"Company Email Format - {employer}"] = f"https://www.google.com/search?q=site:{encoded_employer}+\"@{encoded_employer}\"+email+format"
            
    if self.results["subject_info"].get("education"):
        for school in self.results["subject_info"]["education"]:
            encoded_school = quote_plus(school)
            google_dorks[f"School Records - {school}"] = f"https://www.google.com/search?q=site:{encoded_school}+intext:{encoded_name}+student+OR+alumni+OR+graduate"
            
    # Add all dorking searches to results
    for dork_name, url in google_dorks.items():
        self.results["search_results"][dork_name] = {
            "url": url,
            "category": "Google Dorks",
            "info": f"Advanced Google search: {dork_name}"
        }
        print(f"✓ Generated dork: {dork_name}")
    
    return len(google_dorks)

def search_dark_web_indicators(self):
    """Generate searches for dark web and data breach indicators"""
    print("\nGenerating dark web and breach indicator searches...")
    
    name = self.results["subject_info"]["name"]
    encoded_name = quote_plus(name)
    
    # Create searches for breach databases and indicators
    dark_web_searches = {
        "DeHashed Search": "https://dehashed.com/search?query=",
        "BreachDirectory": "https://breachdirectory.org/",
        "Intelligence X": "https://intelx.io/",
        "Breach Forums Search": "https://breachforums.is/",
        "HaveIBeenPwned": "https://haveibeenpwned.com/"
    }
    
    # Add descriptive information for each search
    for site_name, url in dark_web_searches.items():
        self.results["search_results"][site_name] = {
            "url": url,
            "category": "Data Breach Resources",
            "info": f"Check {site_name} manually for breached data related to {name}"
        }
        print(f"✓ Generated {site_name} reference")
    
    # Add generic Google searches for breach indicators
    breach_indicators = {
        f"Data Breach Indicators - {name}": f"https://www.google.com/search?q={encoded_name}+\"data+breach\"+OR+\"leaked\"+OR+\"compromised\"+OR+\"exposed\"",
        f"Credential Leaks - {name}": f"https://www.google.com/search?q={encoded_name}+\"password\"+\"leak\"+OR+\"credential\"+OR+\"database\""
    }
    
    # Add email-specific breach searches if available
    if self.results["subject_info"].get("emails"):
        for email in self.results["subject_info"]["emails"]:
            encoded_email = quote_plus(email)
            breach_indicators[f"Email Breach - {email}"] = f"https://www.google.com/search?q={encoded_email}+\"breach\"+OR+\"leaked\"+OR+\"compromised\"+OR+\"dump\"" 
    
    # Add phone-specific breach searches if available
    if self.results["subject_info"].get("phones"):
        for phone in self.results["subject_info"]["phones"]:
            phone_clean = re.sub(r'\D', '', phone)
            breach_indicators[f"Phone Breach - {phone}"] = f"https://www.google.com/search?q={phone_clean}+\"breach\"+OR+\"leaked\"+OR+\"compromised\"" 
    
    # Add all breach indicator searches to results
    for indicator_name, url in breach_indicators.items():
        self.results["search_results"][indicator_name] = {
            "url": url,
            "category": "Data Breach Indicators",
            "info": f"Search for breach indicators: {indicator_name}"
        }
        print(f"✓ Generated indicator search: {indicator_name}")
    
    return len(dark_web_searches) + len(breach_indicators)

def search_archived_content(self):
    """Search for archived content in web archives"""
    print("\nGenerating web archive searches...")
    
    name = self.results["subject_info"]["name"]
    encoded_name = quote_plus(name)
    
    # Base archive searches
    archive_searches = {
        "Wayback Machine Name Search": f"https://web.archive.org/web/*/{encoded_name}",
        "Archive.today Name Search": f"https://archive.ph/?q={encoded_name}"
    }
    
    # Add social media archive searches if usernames are available
    if self.results["subject_info"].get("usernames"):
        for username in self.results["subject_info"]["usernames"]:
            encoded_username = quote_plus(username)
            archive_searches[f"Wayback - Twitter/{username}"] = f"https://web.archive.org/web/*/twitter.com/{encoded_username}"
            archive_searches[f"Wayback - Instagram/{username}"] = f"https://web.archive.org/web/*/instagram.com/{encoded_username}"
            archive_searches[f"Wayback - Facebook/{username}"] = f"https://web.archive.org/web/*/facebook.com/{encoded_username}"
    
    # Add website archive searches if domain names can be extracted from emails
    if self.results["subject_info"].get("emails"):
        domains = set()
        for email in self.results["subject_info"]["emails"]:
            if '@' in email:
                domain = email.split('@')[-1]
                domains.add(domain)
        
        for domain in domains:
            archive_searches[f"Wayback - {domain}"] = f"https://web.archive.org/web/*/{domain}"
            archive_searches[f"Archive.today - {domain}"] = f"https://archive.ph/domain/{domain}"
    
    # Add all archive searches to results
    for archive_name, url in archive_searches.items():
        self.results["search_results"][archive_name] = {
            "url": url,
            "category": "Web Archives",
            "info": f"Archived content search: {archive_name}"
        }
        print(f"✓ Generated archive search: {archive_name}")
    
    return len(archive_searches)

def search_professional_networks(self):
    """Search for professional information and company connections"""
    print("\nGenerating professional network searches...")
    
    name = self.results["subject_info"]["name"]
    encoded_name = quote_plus(name)
    
    # Base professional network searches
    professional_searches = {
        "LinkedIn Advanced": f"https://www.google.com/search?q=site:linkedin.com+inurl:in+OR+inurl:pub+-inurl:dir+{encoded_name}",
        "GitHub Profile": f"https://github.com/search?q={encoded_name}&type=users",
        "GitLab Profile": f"https://www.google.com/search?q=site:gitlab.com+{encoded_name}",
        "Medium Articles": f"https://medium.com/search?q={encoded_name}",
        "SlideShare Presentations": f"https://www.slideshare.net/search/slideshow?q={encoded_name}",
        "Speaker Deck": f"https://speakerdeck.com/search?q={encoded_name}",
        "Conference Speakers": f"https://www.google.com/search?q={encoded_name}+\"speaker\"+OR+\"presenter\"+OR+\"panelist\"+filetype:pdf"
    }
    
    # Add company-specific searches if employers are available
    if self.results["subject_info"].get("employers"):
        for employer in self.results["subject_info"]["employers"]:
            encoded_employer = quote_plus(employer)
            professional_searches[f"Company Connection - {employer}"] = f"https://www.google.com/search?q=site:linkedin.com+{encoded_name}+{encoded_employer}"
            professional_searches[f"Corporate Bio - {employer}"] = f"https://www.google.com/search?q=site:{encoded_employer}+{encoded_name}+\"biography\"+OR+\"profile\"+OR+\"about\""
    
    # Add all professional searches to results
    for search_name, url in professional_searches.items():
        self.results["search_results"][search_name] = {
            "url": url,
            "category": "Professional Networks",
            "info": f"Professional information search: {search_name}"
        }
        print(f"✓ Generated professional search: {search_name}")
    
    return len(professional_searches)

def search_person(self):
    """Enhanced main search function that coordinates various search methods"""
    if not self.results["subject_info"].get("name"):
        print("Error: Name is required for the search.")
        return False
        
    print("\n" + "=" * 60)
    print(f"STARTING COMPREHENSIVE OSINT SEARCH FOR: {self.results['subject_info']['name']}")
    print("=" * 60)
    
    # Original search methods
    print("\nSearching social media platforms...")
    self.search_social_media()
    
    print("\nSearching people directories and public records...")
    self.search_people_directories()
    
    # NEW: Advanced Google dorking
    name = self.results["subject_info"]["name"]
    dork_count = self.perform_google_dorking(name)
    print(f"Generated {dork_count} Google dork searches")
    
    # NEW: Dark web and breach indicators
    breach_count = self.search_dark_web_indicators()
    print(f"Generated {breach_count} breach indicator resources")
    
    # NEW: Archived content searches
    archive_count = self.search_archived_content()
    print(f"Generated {archive_count} web archive searches")
    
    # NEW: Professional network searches
    professional_count = self.search_professional_networks()
    print(f"Generated {professional_count} professional network searches")
    
    # Continue with original search methods
    if self.results["subject_info"].get("emails"):
        print("\nSearching by email addresses...")
        for email in self.results["subject_info"]["emails"]:
            self.search_by_email(email)
    
    if self.results["subject_info"].get("phones"):
        print("\nSearching by phone numbers...")
        for phone in self.results["subject_info"]["phones"]:
            self.search_by_phone(phone)
    
    if self.results["subject_info"].get("usernames"):
        print("\nSearching by usernames...")
        for username in self.results["subject_info"]["usernames"]:
            self.search_by_username(username)
    
    if self.results["subject_info"].get("employers"):
        print("\nSearching by employment information...")
        for employer in self.results["subject_info"]["employers"]:
            self.search_by_employer(employer)
    
    if self.results["subject_info"].get("education"):
        print("\nSearching by educational information...")
        for school in self.results["subject_info"]["education"]:
            self.search_by_education(school)
    
    if self.results["subject_info"].get("photo_path"):
        print("\nPerforming reverse image search...")
        self.reverse_image_search()
    
    if self.results["subject_info"].get("relatives"):
        print("\nSearching for information about relatives...")
        for relative in self.results["subject_info"]["relatives"]:
            self.search_by_relative(relative)
    
    # Update metadata
    self.results["metadata"]["search_count"] = len(self.results["search_results"])
    
    # Save results
    self.save_results()
    
    # Display results
    self.display_results()
    
    # Open results in browser if requested
    if self.results["metadata"].get("open_browser"):
        self.open_results_in_browser()
    
    return True

def main():
    parser = argparse.ArgumentParser(description="Enhanced OSINT Search Tool")
    parser.add_argument("--interactive", "-i", action="store_true", help="Run in interactive mode")
    parser.add_argument("--name", "-n", help="Subject's full name")
    parser.add_argument("--birth", "-b", help="Birth date (YYYY-MM-DD)")
    parser.add_argument("--address", "-a", action="append", help="Address (can be used multiple times)")
    parser.add_argument("--email", "-e", action="append", help="Email address (can be used multiple times)")
    parser.add_argument("--phone", "-p", action="append", help="Phone number (can be used multiple times)")
    parser.add_argument("--username", "-u", action="append", help="Username (can be used multiple times)")
    parser.add_argument("--employer", action="append", help="Employer (can be used multiple times)")
    parser.add_argument("--education", action="append", help="Educational institution (can be used multiple times)")
    parser.add_argument("--relative", action="append", help="Relative (can be used multiple times)")
    parser.add_argument("--photo", help="Path to photo for reverse image search")
    parser.add_argument("--output", "-o", help="Output file name (without extension)")
    parser.add_argument("--format", "-f", choices=["json", "txt"], default="json", help="Output format (json or txt)")
    parser.add_argument("--browser", action="store_true", help="Open results in browser")
    parser.add_argument("--dorking", "-d", action="store_true", help="Enable advanced Google dorking")
    parser.add_argument("--archives", action="store_true", help="Search web archives")
    parser.add_argument("--breaches", action="store_true", help="Check for data breach indicators")
    parser.add_argument("--professional", action="store_true", help="Search professional networks")
    parser.add_argument("--all", action="store_true", help="Enable all advanced search features")
    
    args = parser.parse_args()
    
    searcher = EnhancedOSINTSearcher()
    
    # Check for interactive mode
    if args.interactive or len(sys.argv) == 1:
        if searcher.interactive_mode():
            searcher.search_person()
    else:
        # Use command line arguments
        if not args.name:
            print("Error: Name is required when not in interactive mode.")
            parser.print_help()
            return
            
        # Set up subject info
        searcher.results["subject_info"]["name"] = args.name
        
        if args.birth:
            searcher.results["subject_info"]["birth"] = {"date": args.birth}
            
        if args.address:
            searcher.results["subject_info"]["addresses"] = args.address
            
        if args.email:
            searcher.results["subject_info"]["emails"] = args.email
            
        if args.phone:
            searcher.results["subject_info"]["phones"] = args.phone
            
        if args.username:
            searcher.results["subject_info"]["usernames"] = args.username
            
        if args.employer:
            searcher.results["subject_info"]["employers"] = args.employer
            
        if args.education:
            searcher.results["subject_info"]["education"] = args.education
            
        if args.relative:
            searcher.results["subject_info"]["relatives"] = args.relative
            
        if args.photo and os.path.exists(args.photo):
            searcher.results["subject_info"]["photo_path"] = args.photo
            
        # Set output options
        if args.output:
            searcher.output_file = args.output
        else:
            searcher.output_file = f"osint_{args.name.replace(' ', '_').lower()}_{int(time.time())}"
            
        searcher.results["metadata"]["output_format"] = args.format
        searcher.results["metadata"]["open_browser"] = args.browser
        
        # Set advanced search options
        searcher.results["metadata"]["use_dorking"] = args.dorking or args.all
        searcher.results["metadata"]["search_archives"] = args.archives or args.all
        searcher.results["metadata"]["check_breaches"] = args.breaches or args.all
        searcher.results["metadata"]["search_professional"] = args.professional or args.all
        
        # Run search
        searcher.search_person()

if __name__ == "__main__":
    main()
