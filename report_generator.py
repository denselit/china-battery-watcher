from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.lib.pagesizes import A4

import os
from datetime import datetime



class ReportGenerator:


    def __init__(
        self,
        output_dir="reports"
    ):


        self.output_dir = output_dir


        if not os.path.exists(
            self.output_dir
        ):

            os.makedirs(
                self.output_dir
            )



    def generate(
        self,
        articles
    ):


        filename = (
            "China_Battery_Intelligence_"
            +
            datetime.now().strftime(
                "%Y%m%d"
            )
            +
            ".pdf"
        )



        filepath = os.path.join(
            self.output_dir,
            filename
        )



        document = SimpleDocTemplate(
            filepath,
            pagesize=A4
        )



        styles = getSampleStyleSheet()



        story = []



        # --------------------------------
        # Title
        # --------------------------------


        story.append(
            Paragraph(
                "🔋 China Battery Technology Intelligence Report",
                styles["Title"]
            )
        )


        story.append(
            Spacer(
                1,
                20
            )
        )



        story.append(
            Paragraph(
                "Generated Date: "
                +
                datetime.now().strftime(
                    "%Y-%m-%d"
                ),
                styles["Normal"]
            )
        )



        story.append(
            Spacer(
                1,
                20
            )
        )



        # --------------------------------
        # Executive Summary
        # --------------------------------


        story.append(
            Paragraph(
                "1. Executive Summary",
                styles["Heading2"]
            )
        )



        ranked_articles = sorted(
            articles,
            key=lambda x:
            x.get(
                "investment_score",
                0
            ),
            reverse=True
        )



        if ranked_articles:


            top_articles = ranked_articles[:5]


            for article in top_articles:


                title = article.get(
                    "title",
                    "No title"
                )


                score = article.get(
                    "investment_score",
                    0
                )


                technology = article.get(
                    "technology_category",
                    []
                )



                summary = (

                    f"<b>{title}</b><br/>"
                    f"Technology: {technology}<br/>"
                    f"Investment Score: {score}/100"

                )



                story.append(
                    Paragraph(
                        summary,
                        styles["Normal"]
                    )
                )


                story.append(
                    Spacer(
                        1,
                        10
                    )
                )



        else:

            story.append(
                Paragraph(
                    "No classified articles available.",
                    styles["Normal"]
                )
            )



        story.append(
            PageBreak()
        )



        # --------------------------------
        # Technology Radar
        # --------------------------------


        story.append(
            Paragraph(
                "2. Technology Radar",
                styles["Heading2"]
            )
        )



        technology_map = {}



        for article in articles:


            categories = article.get(
                "technology_category",
                []
            )


            for tech in categories:


                if tech not in technology_map:

                    technology_map[tech] = []



                technology_map[tech].append(
                    article
                )



        for tech, items in technology_map.items():


            story.append(
                Paragraph(
                    tech,
                    styles["Heading3"]
                )
            )


            story.append(
                Paragraph(
                    f"Related Articles: {len(items)}",
                    styles["Normal"]
                )
            )



            avg_score = sum(

                item.get(
                    "investment_score",
                    0
                )

                for item in items

            ) / len(items)



            story.append(
                Paragraph(
                    f"Average Investment Score: {avg_score:.1f}/100",
                    styles["Normal"]
                )
            )



            story.append(
                Spacer(
                    1,
                    15
                )
            )



        story.append(
            PageBreak()
        )



        # --------------------------------
        # Investment Ranking
        # --------------------------------


        story.append(
            Paragraph(
                "3. Investment Priority Ranking",
                styles["Heading2"]
            )
        )



        for index, article in enumerate(
            ranked_articles,
            start=1
        ):


            title = article.get(
                "title",
                ""
            )


            score = article.get(
                "investment_score",
                0
            )


            if score >= 40:

                signal = "HIGH PRIORITY"


            elif score >= 20:

                signal = "WATCH"


            else:

                signal = "MONITOR"



            text = (

                f"{index}. {title}<br/>"
                f"Score: {score}/100<br/>"
                f"Signal: {signal}"

            )



            story.append(
                Paragraph(
                    text,
                    styles["Normal"]
                )
            )


            story.append(
                Spacer(
                    1,
                    10
                )
            )



        story.append(
            PageBreak()
        )



        # --------------------------------
        # Detailed Articles
        # --------------------------------


        story.append(
            Paragraph(
                "4. Detailed Article Analysis",
                styles["Heading2"]
            )
        )



        for article in articles:


            title = article.get(
                "title",
                "No title"
            )


            source = article.get(
                "source",
                ""
            )


            technology = article.get(
                "technology_category",
                []
            )


            score = article.get(
                "investment_score",
                0
            )


            content = article.get(
                "content",
                "No content"
            )



            story.append(
                Paragraph(
                    title,
                    styles["Heading3"]
                )
            )



            story.append(
                Paragraph(
                    f"Source: {source}",
                    styles["Normal"]
                )
            )


            story.append(
                Paragraph(
                    f"Technology: {technology}",
                    styles["Normal"]
                )
            )


            story.append(
                Paragraph(
                    f"Investment Score: {score}/100",
                    styles["Normal"]
                )
            )


            story.append(
                Spacer(
                    1,
                    10
                )
            )



            story.append(
                Paragraph(
                    content[:2000],
                    styles["Normal"]
                )
            )


            story.append(
                Spacer(
                    1,
                    20
                )
            )



        document.build(
            story
        )



        return filepath
