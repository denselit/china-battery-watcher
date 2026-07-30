from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

from datetime import datetime
import os



class ReportGenerator:


    def __init__(
        self,
        output_folder
    ):

        self.output_folder = output_folder


        if not os.path.exists(
            output_folder
        ):

            os.makedirs(
                output_folder
            )


        # Korean font support

        pdfmetrics.registerFont(
            UnicodeCIDFont(
                "HYSMyeongJo-Medium"
            )
        )



    def generate(
        self,
        articles
    ):


        today = datetime.now().strftime(
            "%Y-%m-%d"
        )


        filename = (

            "China_Battery_Report_"
            +
            today
            +
            ".pdf"

        )


        filepath = os.path.join(
            self.output_folder,
            filename
        )



        document = SimpleDocTemplate(
            filepath
        )



        styles = getSampleStyleSheet()


        for style in styles.byName.values():

            style.fontName = (
                "HYSMyeongJo-Medium"
            )



        content = []



        # Title

        content.append(
            Paragraph(
                "China Battery Technology Weekly Report",
                styles["Title"]
            )
        )


        content.append(
            Spacer(
                1,
                20
            )
        )


        content.append(
            Paragraph(
                f"Generated Date: {today}",
                styles["Normal"]
            )
        )


        content.append(
            Spacer(
                1,
                20
            )
        )



        # Articles

        for index, article in enumerate(
            articles,
            start=1
        ):


            content.append(
                Paragraph(
                    f"{index}. {article.get('title','')}",
                    styles["Heading2"]
                )
            )


            content.append(
                Spacer(
                    1,
                    10
                )
            )



            tech = ", ".join(
                article.get(
                    "technology_keywords",
                    []
                )
            )


            content.append(
                Paragraph(
                    f"Technology: {tech}",
                    styles["Normal"]
                )
            )



            content.append(
                Spacer(
                    1,
                    10
                )
            )


            content.append(
                Paragraph(
                    "Summary: Technical summary will be generated.",
                    styles["Normal"]
                )
            )


            content.append(
                Spacer(
                    1,
                    10
                )
            )



            content.append(
                Paragraph(
                    "Source: "
                    +
                    article.get(
                        "source",
                        ""
                    ),
                    styles["Normal"]
                )
            )


            content.append(
                Paragraph(
                    "Link: "
                    +
                    article.get(
                        "link",
                        ""
                    ),
                    styles["Normal"]
                )
            )


            content.append(
                Spacer(
                    1,
                    20
                )
            )



        document.build(
            content
        )


        return filepath
