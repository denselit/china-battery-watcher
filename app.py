import streamlit as st
import os

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

    Purpose:
    Information discovery and research support.
    """
)



if st.button(
    "🔍 Collect Latest Information"
):


    with st.spinner(
        "Collecting battery technology information..."
    ):


        # Collect

        collector = BatteryCollector(
            "keywords.yaml"
        )

        articles = collector.collect_articles()



        st.success(
            f"Collected articles: {len(articles)}"
        )



        # Filter

        keyword_filter = KeywordFilter(
            "keywords.yaml"
        )

        filtered_articles = (
            keyword_filter.filter_articles(
                articles
            )
        )



        st.info(
            f"Technology-related articles: {len(filtered_articles)}"
        )



        # Save report

        generator = ReportGenerator(
            "reports"
        )


        report_file = generator.generate(
            filtered_articles
        )



        st.session_state[
            "report_file"
        ] = report_file



        st.session_state[
            "articles"
        ] = filtered_articles



# -------------------------
# Article Viewer
# -------------------------

if "articles" in st.session_state:


    st.subheader(
        "📚 Technology Watch Results"
    )


    for article in st.session_state["articles"]:


        with st.expander(
            article["title"]
        ):


            st.write(
                "Technology Keywords:"
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


            st.link_button(
                "Open Article",
                article["link"]
            )



# -------------------------
# Report Viewer
# -------------------------

if "report_file" in st.session_state:


    st.divider()


    st.subheader(
        "📄 Weekly Report"
    )


    report_path = st.session_state[
        "report_file"
    ]


    if os.path.exists(
        report_path
    ):


        with open(
            report_path,
            "r",
            encoding="utf-8"
        ) as file:

            report_content = file.read()



        st.markdown(
            report_content
        )



        st.download_button(

            label=
            "⬇️ Download Weekly Report",

            data=
            report_content,

            file_name=
            "china_battery_weekly_report.md",

            mime=
            "text/markdown"

        )
