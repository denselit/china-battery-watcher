class TechnologyClassifier:


    def __init__(self):

        self.rules = {

            "Sodium-ion": [
                "sodium",
                "na-ion",
                "sodium ion"
            ],

            "LFP": [
                "lfp",
                "lithium iron phosphate",
                "lifepo4"
            ],

            "LMR": [
                "lithium-rich manganese",
                "lmr",
                "high manganese"
            ],

            "Solid-state": [
                "solid state",
                "solid-state",
                "solid electrolyte"
            ],

            "ESS": [
                "bess",
                "energy storage",
                "stationary storage"
            ],

            "Battery Recycling": [
                "recycling",
                "black mass",
                "battery recovery"
            ],

            "Cathode Material": [
                "cathode",
                "precursor",
                "nickel",
                "manganese"
            ]

        }



    def classify(self, article):


        text = (
            article.get("title", "")
            +
            " "
            +
            article.get("content", "")
        ).lower()



        technologies = []



        score = 0



        for tech, keywords in self.rules.items():

            for keyword in keywords:

                if keyword in text:

                    technologies.append(
                        tech
                    )

                    break



        # Remove duplicate categories

        technologies = list(
            set(technologies)
        )



        # Investment relevance scoring

        if "Sodium-ion" in technologies:

            score += 25


        if "LMR" in technologies:

            score += 25


        if "Solid-state" in technologies:

            score += 20


        if "ESS" in technologies:

            score += 15


        if "LFP" in technologies:

            score += 10



        # Commercial signals

        commercial_words = [

            "factory",
            "gigafactory",
            "production",
            "deployment",
            "commercial",
            "agreement",
            "investment"

        ]



        for word in commercial_words:

            if word in text:

                score += 5
                break



        if score > 100:

            score = 100



        return {

            "technology_category":
                technologies,


            "investment_score":
                score

        }
