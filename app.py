# TEST123
import streamlit as st
import os


from collector import BatteryCollector
from keyword_filter import KeywordFilter
from article_extractor import ArticleExtractor
from report_generator import ReportGenerator
from technology_classifier import TechnologyClassifier
from deduplicator import ArticleDeduplicator



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

    Current stage:
    Collection → Deduplication → Filtering → Extraction → Technology Classification → PDF Report
    """
)



# -------------------------
# Main Process
# -------------------------

if st.button(
    "🔍 Collect Latest Information"
):


    with st.spinner(
        "Collecting and analyzing articles..."
    ):



        # 1. Collect

        collector = BatteryCollector(
            "keywords.yaml"
        )


        articles = collector.collect_articles()



        st.success(
            f"Collected articles: {len(articles)}"
        )



        # 2. Deduplicate
        # (Same article often shows up under multiple keyword searches,
        # e.g. both a company keyword and a technology keyword. Doing
        # this before filtering/extraction avoids re-scraping and
        # re-analyzing the same article multiple times.)

        deduplicator = ArticleDeduplicator()

        deduplicated_articles = deduplicator.remove_duplicates(
            articles
        )

        st.info(
            f"After deduplication: {len(deduplicated_articles)} unique articles"
        )



        # 3. Filter

        keyword_filter = KeywordFilter(
            "keywords.yaml"
        )


        filtered_articles = (
            keyword_filter.filter_articles(
                deduplicated_articles
            )
        )



        st.info(
            f"Technology articles: {len(filtered_articles)}"
        )



        # 4. Extract Article Content

        extractor = ArticleExtractor()


        classifier = TechnologyClassifier()



        extracted_articles = []



        progress = st.progress(0)



        total = len(
            filtered_articles
        )



        for index, article in enumerate(
            filtered_articles
        ):


            result = extractor.extract(
                article
            )



            # 5. Technology Classification

            classification = classifier.classify(
                result
            )



            result.update(
                classification
            )



            extracted_articles.append(
                result
            )



            progress.progress(
                (index + 1) / total
            )



        st.success(
            "Article extraction and technology classification completed."
        )



        # Save

        st.session_state[
            "articles"
        ] = extracted_articles



        # 6. Generate PDF

        generator = ReportGenerator(
            "reports"
        )


        report_file = generator.generate(
            extracted_articles
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
                "Source:"
            )


            st.write(
                article.get(
                    "source",
                    ""
                )
            )



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
                "Technology Category:"
            )


            st.write(
                article.get(
                    "technology_category",
                    []
                )
            )



            st.write(
                "Investment Score:"
            )


            st.write(
                article.get(
                    "investment_score",
                    0
                )
            )



            st.write(
                "Extracted Content Preview:"
            )



            content = article.get(
                "content",
                ""
            )



            if content:


                st.write(
                    content[:1000]
                )


            else:

                st.warning(
                    "No content extracted."
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
# PDF Download
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
