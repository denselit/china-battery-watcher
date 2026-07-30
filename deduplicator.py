from difflib import SequenceMatcher



class ArticleDeduplicator:


    def __init__(
        self,
        similarity_threshold=0.85
    ):

        self.threshold = similarity_threshold



    def normalize_title(
        self,
        title
    ):

        if not title:
            return ""


        title = title.lower()


        remove_words = [

            "-",
            ":",
            "|",
            ".",
            ",",
            "the",
            "a",
            "an"

        ]


        for word in remove_words:

            title = title.replace(
                word,
                ""
            )


        return title.strip()



    def similarity(
        self,
        title1,
        title2
    ):


        return SequenceMatcher(
            None,
            title1,
            title2
        ).ratio()



    def remove_duplicates(
        self,
        articles
    ):


        unique_articles = []


        seen_titles = []



        for article in articles:


            title = self.normalize_title(
                article.get(
                    "title",
                    ""
                )
            )



            duplicate = False



            for seen in seen_titles:


                score = self.similarity(
                    title,
                    seen
                )


                if score >= self.threshold:

                    duplicate = True

                    break



            if not duplicate:


                unique_articles.append(
                    article
                )


                seen_titles.append(
                    title
                )



        return unique_articles
