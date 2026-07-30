import yaml



class KeywordFilter:


    def __init__(self, keyword_file):

        with open(
            keyword_file,
            "r",
            encoding="utf-8"
        ) as file:

            self.keywords = yaml.safe_load(file)



    def get_all_technology_keywords(self):

        keywords = []


        for tech_list in self.keywords["technologies"].values():

            keywords.extend(
                tech_list
            )


        return keywords



    def filter_articles(self, articles):

        technology_keywords = (
            self.get_all_technology_keywords()
        )


        filtered_articles = []


        for article in articles:


            text = (
                article["title"]
                +
                " "
                +
                article["keyword"]
            ).lower()



            matched = []


            for keyword in technology_keywords:


                if keyword.lower() in text:

                    matched.append(
                        keyword
                    )



            if matched:


                article["technology_keywords"] = matched


                filtered_articles.append(
                    article
                )


        return filtered_articles
