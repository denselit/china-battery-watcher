import streamlit as st

from collector import BatteryCollector
from keyword_filter import KeywordFilter
from report_generator import ReportGenerator



st.set_page_config(
    page_title="China Battery Watcher",
    layout="wide"
)



st.title(
    "🔋 China Battery Technology Watcher"
)


st.write(
    """
    Personal research assistant for monitoring:

    - CATL
    - BYD
    - LFP
    - LMR
    - Sodium-ion battery

    AI is used to support information gathering,
    not replace technical judgment.
    """
)



if st.button(
    "🔍 Collect Latest Information"
):


    with st.spinner(
        "Collecting battery technology news..."
    ):


        # 1. Collect

        collector = BatteryCollector(
            "keywords.yaml"
        )


        articles = collector.collect_articles()



        st.success(
            f"Collected {len(articles)} articles"
        )



        # 2. Filter

        filter_agent = KeywordFilter(
            "keywords.yaml"
        )


        filtered_articles = (
            filter_agent.filter_articles(
                articles
            )
        )



        st.info(
            f"Relevant technology articles: {len(filtered_articles)}"
        )



        # 3. Display


        st.subheader(
            "Technology Watch Results"
        )


        for article in filtered_articles:


            with st.expander(
                article["title"]
            ):


                st.write(
                    "Keyword:"
                )

                st.write(
                    article.get(
                        "technology_keywords",
                        []
                    )
                )


                st.write(
                    "Source:"
                )

                st.write(
                    article.get(
                        "source",
                        ""
                    )
                )


                st.write(
                    "Link:"
                )

                st.write(
                    article.get(
                        "link",
                        ""
                    )
                )



        # 4. Generate report

        generator = ReportGenerator(
            "reports"
        )


        report_file = generator.generate(
            filtered_articles
        )


        st.success(
            "Weekly report generated!"
        )


        st.write(
            report_file
        )
