import streamlit as st
import os

from collector import BatteryCollector
from keyword_filter import KeywordFilter
from report_generator import ReportGenerator


# -------------------------
# Page Configuration
# -------------------------

st.set_page_config(
    page_title="China Battery Watcher",
    layout="wide"
)


# -------------------------
# Title
# -------------------------

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
    - Sodium-ion Battery

    Purpose:
    Technical information collection and research support.
    """
)


# -------------------------
# Collect Button
# -------------------------

if st.button(
    "🔍 Collect Latest Information"
):

    with st.spinner(
        "Collecting battery technology information..."
    ):


        # -------------------------
        # 1. Collect Articles
        # -------------------------

        collector = BatteryCollector(
            "keywords.yaml"
        )


        articles = collector.collect_articles()


        st.success(
            f"Collected articles: {len(articles)}"
        )


        # -------------------------
        # 2. Filter Technology Articles
        # -------------------------

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


        # Save to Session

        st.session_state[
            "articles"
        ] = filtered_articles



        # -------------------------
        # 3. Generate PDF Report
        # -------------------------

        generator = ReportGenerator(
            "reports"
        )


        report_file = generator.generate(
            filtered_articles
        )


        st.session_state[
            "report_file"
        ] = report_file



# -------------------------
# Article Viewer
# -------------------------

if "articles" in st.session_state:


    st.divider()


    st.subheader(
        "📚 Technology Watch Results"
    )


    for article in st.session_state["articles"]:


        with st.expander(
            article.get(
                "title",
                "No title"
            )
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


            if article.get(
                "link",
                ""
            ):


                st.link_button(
                    "Open Original Article",
                    article["link"]
                )



# -------------------------
# PDF Report Viewer
# -------------------------

if "report_file" in st.session_state:


    st.divider()


    st.subheader(
        "📄 Weekly PDF Report"
    )


    report_path = st.session_state[
        "report_file"
    ]


    if os.path.exists(
        report_path
    ):


        st.success(
            "PDF Report generated successfully!"
        )


        st.write(
            f"File location: {report_path}"
        )


        with open(
            report_path,
            "rb"
        ) as pdf_file:


            st.download_button(

                label=
                "⬇️ Download PDF Report",

                data=
                pdf_file,

                file_name=
                os.path.basename(
                    report_path
                ),

                mime=
                "application/pdf"

            )
