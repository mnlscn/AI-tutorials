# Import all the required libraries
import os
import requests
from dotenv import load_dotenv
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import HumanMessagePromptTemplate, ChatPromptTemplate
from pydantic import BaseModel, Field
from bs4 import BeautifulSoup
from langchain_openai.chat_models import ChatOpenAI

load_dotenv()
import warnings
warnings.filterwarnings(action="ignore")


class ProductDetails(BaseModel):
    """
    This class is used to capture additional product details related to Mobile
    """

    RAM: int = Field(description="RAM of the mobile")
    ROM: int = Field(description="ROM of the mobile")
    Battery: int = Field(description="Battery capacity of the mobile")

class Product(BaseModel):
    """
    This class is used to capture primary product details of Mobile
    """
    Name: str = Field(description="Name of the mobile")
    Price: int = Field(description="Price of the mobile")
    Details: ProductDetails = Field(description="Additional features of the Mobile")


class Products(BaseModel):
    """
    This class is used to store the collection/list of Mobiles
    """
    Mobiles: list[Product] = Field("List of mobiles listed in the text")


model = ChatOpenAI(temperature=0, model="gpt-4o-mini")

# Declare your url or website for extracting data
url = "https://www.flipkart.com/search?q=samsung+s23&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&p%5B%5D=facets.ram%255B%255D%3D8%2BGB%2Band%2BAbove&p%5B%5D=facets.battery_capacity%255B%255D%3D5000%2B-%2B5999%2BmAh"


# Store the HTML text to a variable
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
html_text = soup.body.text

print(html_text)

output_parser = PydanticOutputParser(pydantic_object=Products)
format_instructions = output_parser.get_format_instructions()


human_text = "{instruction}\n{format_instructions}"
message = HumanMessagePromptTemplate.from_template(human_text)
prompt = ChatPromptTemplate.from_messages([message])

chain = prompt | model | output_parser
products = chain.invoke({"instruction":"Extract all the products from the below text \n" + html_text,"format_instructions":format_instructions})


# Displaying the list of products/Mobiles in an object oriented way
products.Mobiles



