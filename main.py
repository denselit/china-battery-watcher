from collector import BatteryCollector
from keyword_filter import KeywordFilter
from report_generator import ReportGenerator



def main():


    print(
        "Starting China Battery Technology Watcher..."
    )


    # 1. Collect articles

    collector = BatteryCollector(
        "keywords.yaml"
    )


    articles = collector.collect_articles()


    print(
        f"Collected articles: {len(articles)}"
    )



    # 2. Filter technology-related articles

    keyword_filter = KeywordFilter(
        "keywords.yaml"
    )


    filtered_articles = keyword_filter.filter_articles(
        articles
    )


    print(
        f"Relevant articles: {len(filtered_articles)}"
    )



    # 3. Generate report

    generator = ReportGenerator(
        "reports"
    )


    report_file = generator.generate(
        filtered_articles
    )


    print(
        "Report generated:"
    )


    print(
        report_file
    )



if __name__ == "__main__":

    main()
