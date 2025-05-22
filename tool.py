import os
import requests
from datetime import datetime
from pydantic import BaseModel, Field

class Tools:
    def __init__(self):
        pass

    # Add your custom tools using pure Python code here, make sure to add type hints and descriptions
	
    def get_user_name_and_email_and_id(self, __user__: dict = {}) -> str:
        """
        Get the user name, Email and ID from the user object.
        """

        # Do not include a descrption for __user__ as it should not be shown in the tool's specification
        # The session user object will be passed as a parameter when the function is called

        print(__user__)
        result = ""

        if "name" in __user__:
            result += f"User: {__user__['name']}"
        if "id" in __user__:
            result += f" (ID: {__user__['id']})"
        if "email" in __user__:
            result += f" (Email: {__user__['email']})"

        if result == "":
            result = "User: Unknown"

        return result

    def get_current_time(self) -> str:
        """
        Get the current time in a more human-readable format.
        """

        now = datetime.now()
        current_time = now.strftime("%I:%M:%S %p")  # Using 12-hour format with AM/PM
        current_date = now.strftime(
            "%A, %B %d, %Y"
        )  # Full weekday, month name, day, and year

        return f"Current Date and Time = {current_date}, {current_time}"

    def calculator(
        self,
        equation: str = Field(
            ..., description="The mathematical equation to calculate."
        ),
    ) -> str:
        """
        Calculate the result of an equation.
        """

        # Avoid using eval in production code
        # https://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html
        try:
            result = eval(equation)
            return f"{equation} = {result}"
        except Exception as e:
            print(e)
            return "Invalid equation"

    def get_current_weather(
        self,
        city: str = Field(
            "New York, NY", description="Get the current weather for a given city."
        ),
    ) -> str:
        """
        Get the current weather for a given city.
        """

        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            return (
                "API key is not set in the environment variable 'OPENWEATHER_API_KEY'."
            )

        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric",  # Optional: Use 'imperial' for Fahrenheit
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
            data = response.json()

            if data.get("cod") != 200:
                return f"Error fetching weather data: {data.get('message')}"

            weather_description = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]

            return f"Weather in {city}: {temperature}°C"
        except requests.RequestException as e:
            return f"Error fetching weather data: {str(e)}"
            
    def get_skku_news(
        self,
        limit: int = Field(
            5, description="Number of news items to retrieve (default: 5, max: 10)"
        ),
    ) -> str:
        """
        Get the latest news from Sungkyunkwan University (SKKU) website.
        """
        try:
            import requests
            from bs4 import BeautifulSoup
            
            # Limit the number of news items to a reasonable range
            if limit > 10:
                limit = 10
            
            # SKKU main website URL
            url = "https://www.skku.edu/skku/index.do"
            
            # Send a GET request to the website
            response = requests.get(url)
            response.raise_for_status()
            
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the news section - based on the website structure
            news_section = soup.select('.news-list li')
            
            if not news_section:
                # Try alternative selector if the first one doesn't work
                news_section = soup.select('.main-news-section a')
            
            if not news_section:
                return "Unable to find news content on the SKKU website. The website structure might have changed."
            
            # Extract news items up to the limit
            news_items = []
            count = 0
            
            for item in news_section:
                if count >= limit:
                    break
                    
                # Try to extract the news title and link
                title_element = item.select_one('a')
                if not title_element:
                    title_element = item
                    
                title = title_element.get_text(strip=True)
                link = title_element.get('href', '')
                
                # Fix relative URLs
                if link and not link.startswith(('http://', 'https://')):
                    link = f"https://www.skku.edu{link}" if link.startswith('/') else f"https://www.skku.edu/{link}"
                
                # Add the news item to the list
                if title:
                    news_items.append(f"- {title}\n  Link: {link}")
                    count += 1
            
            if not news_items:
                return "No news items found on the SKKU website."
            
            # Format the news items into a readable string
            formatted_news = "Latest News from Sungkyunkwan University (SKKU):\n\n" + "\n\n".join(news_items)
            return formatted_news
            
        except requests.RequestException as e:
            return f"Error fetching news from SKKU website: {str(e)}"
        except Exception as e:
            return f"An error occurred while processing SKKU news: {str(e)}"