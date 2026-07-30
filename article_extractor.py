import requests

from bs4 import BeautifulSoup



class ArticleExtractor:


    def __init__(self):

        self.headers = {

            "User-Agent":
            "Mozilla/5.0"

        }



    def extract(
        self,
        article
    ):


        url = article.get(
            "link",
            ""
        )


        if not url:

            article["content"] = ""

            return article



        try:


            response = requests.get(

                url,

                headers=self.headers,

                timeout=10

            )


            response.raise_for_status()



            soup = BeautifulSoup(

                response.text,

                "html.parser"

            )



            # Remove unnecessary elements

            for tag in soup(
                [
                    "script",
                    "style",
                    "nav",
                    "footer"
                ]
            ):

                tag.decompose()



            text = soup.get_text(
                separator=" "
            )



            text = " ".join(
                text.split()
            )



            article["content"] = text[:5000]



        except Exception as e:


            article["content"] = (

                "Extraction failed: "
                +
                str(e)

            )



        return article
