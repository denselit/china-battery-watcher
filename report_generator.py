import os
from datetime import datetime



class ReportGenerator:


    def __init__(self, output_folder):

        self.output_folder = output_folder


        if not os.path.exists(
            output_folder
        ):

            os.makedirs(
                output_folder
            )



    def generate(
        self,
        articles
    ):


        today = datetime.now().strftime(
            "%Y-%m-%d"
        )


        report = []



        report.append(
            "# China Battery Weekly Watch\n"
        )


        report.append(
            f"Generated: {today}\n"
        )



        report.append(
            "---\n"
        )



        if len(articles) == 0:


            report.append(
                "No relevant articles found.\n"
            )



        else:


            for article in articles:


                report.append(
                    "## "
                    +
                    article["title"]
                    +
                    "\n"
                )


                report.append(
                    "Technology keywords:\n"
                )


                for keyword in article.get(
                    "technology_keywords",
                    []
                ):

                    report.append(
                        f"- {keyword}\n"
                    )


                report.append(
                    "\nSource:\n"
                )


                report.append(
                    article.get(
                        "source",
                        ""
                    )
                    +
                    "\n"
                )


                report.append(
                    "\nLink:\n"
                )


                report.append(
                    article.get(
                        "link",
                        ""
                    )
                    +
                    "\n"
                )


                report.append(
                    "\n---\n"
                )



        file_path = os.path.join(
            self.output_folder,
            "weekly_report.md"
        )


        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                "\n".join(report)
            )


        return file_path
