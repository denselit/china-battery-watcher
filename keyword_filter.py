import yaml



class KeywordFilter:


    def __init__(self, keyword_file):

        with open(
            keyword_file,
            "r",
            encoding="utf-8"
        ) as f:

            self.config = yaml.safe_load(f)



        self.tech_keywords = [

            "LFP",
            "lithium iron phosphate",
            "sodium-ion",
            "sodium ion",
            "LMR",
            "lithium-rich manganese",
            "lithium rich manganese"

        ]



        self.company_keywords = [

            "CATL",
            "Contemporary Amperex",
            "BYD",
            "FinDreams"

        ]



        self.battery_context = [

            "battery",
            "cell",
            "cathode",
            "anode",
            "electrode",
            "energy density",
            "Wh/kg",
            "GWh",
            "kWh",
            "cycle life",
            "manufacturing",
            "commercial",
            "production"

        ]



    def normalize(self, text):

        if not text:

            return ""

        return text.lower()



    def contains_any(
        self,
        text,
        keywords
    ):

        for k in keywords:

            if k.lower() in text:

                return True

        return False



    def is_valid_article(
        self,
        article
    ):


        title = self.normalize(
            article.get(
                "title",
                ""
            )
        )


        summary = self.normalize(
            article.get(
                "summary",
                ""
            )
        )


        combined = (
            title
            +
            " "
            +
            summary
        )



        # -------------------------
        # LMR special handling
        # -------------------------

        if "lmr" in combined:


            if not self.contains_any(
                combined,
                [
                    "lithium-rich",
                    "lithium rich",
                    "manganese",
                    "cathode"
                ]
            ):

                return False



        # -------------------------
        # Technology detection
        # -------------------------

        has_technology = (
            self.contains_any(
                combined,
                self.tech_keywords
            )
        )



        if not has_technology:

            return False



        # -------------------------
        # Battery context check
        # -------------------------

        has_context = (
            self.contains_any(
                combined,
                self.battery_context
            )
        )



        if not has_context:

            return False



        return True




    def filter_articles(
        self,
        articles
    ):


        results = []


        for article in articles:


            if self.is_valid_article(
                article
            ):


                results.append(
                    article
                )


        return results
