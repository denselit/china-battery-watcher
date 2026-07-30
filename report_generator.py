import os
from datetime import datetime
from collections import Counter

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle,
    HRFlowable,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm

from article_analyzer import ArticleAnalyzer


# Track grouping. Adjust freely -- this mirrors the 4-track structure
# (Na-ion / LMR / LFP / raw materials & supply chain) commonly used
# for Chinese battery trend reporting.
TRACKS = {
    "Sodium-ion": ["Sodium-ion"],
    "LMR (Lithium-rich Manganese)": ["LMR"],
    "LFP": ["LFP", "LMFP"],
    "Materials & Supply Chain": ["Cathode Material", "Battery Recycling"],
}
OTHER_TRACK = "Other / Emerging Tech"

IMPORTANCE_LABELS = {
    5: "INDUSTRY CHANGING",
    4: "MAJOR",
    3: "IMPORTANT",
    2: "USEFUL",
    1: "MINOR",
    0: "UNRATED",
}


class ReportGenerator:
    """
    Generates the PDF intelligence report.

    Unlike the previous version, this pulls structured facts
    (companies, technologies, materials, event type, investment
    implication, importance 1-5) from ArticleAnalyzer instead of
    dumping raw scraped text. Ranking is driven primarily by the
    LLM's importance rating rather than a keyword-hit count.
    """

    def __init__(self, output_dir="reports", use_llm_analysis=True):
        self.output_dir = output_dir
        self.use_llm_analysis = use_llm_analysis
        self.analyzer = ArticleAnalyzer() if use_llm_analysis else None

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        self.styles = getSampleStyleSheet()
        self._register_custom_styles()

    def _register_custom_styles(self):
        self.styles.add(ParagraphStyle(
            name="ArticleBody", parent=self.styles["Normal"],
            fontSize=9.5, leading=13
        ))
        self.styles.add(ParagraphStyle(
            name="FactLabel", parent=self.styles["Normal"],
            fontSize=9, textColor=colors.HexColor("#555555")
        ))
        self.styles.add(ParagraphStyle(
            name="TrackHeader", parent=self.styles["Heading2"],
            textColor=colors.HexColor("#0B3D91")
        ))

    def _enrich(self, articles):
        """Attach LLM-extracted structured facts to each article.

        Skips re-analysis if an article already carries a non-empty
        'facts' dict, so re-generating a report from cached article
        data doesn't burn API calls again.
        """
        enriched = []
        for article in articles:
            merged = dict(article)
            if merged.get("facts"):
                enriched.append(merged)
                continue
            facts = {}
            if self.use_llm_analysis:
                try:
                    facts = self.analyzer.analyze(article)
                except Exception:
                    facts = {}
            merged["facts"] = facts
            enriched.append(merged)
        return enriched

    def _track_for(self, article):
        cats = article.get("technology_category", [])
        for track_name, members in TRACKS.items():
            if any(c in members for c in cats):
                return track_name
        return OTHER_TRACK

    def _priority_score(self, article):
        """Blend the keyword-based score with LLM importance for ranking.

        Importance (1-5) is weighted heavily since it reflects actual
        reading of the article rather than keyword presence.
        """
        base = article.get("investment_score", 0)
        importance = article.get("facts", {}).get("importance", 0) or 0
        return base + importance * 15

    def generate(self, articles):
        articles = self._enrich(articles)

        filename = (
            "China_Battery_Intelligence_"
            + datetime.now().strftime("%Y%m%d")
            + ".pdf"
        )
        filepath = os.path.join(self.output_dir, filename)

        document = SimpleDocTemplate(
            filepath, pagesize=A4, topMargin=20 * mm, bottomMargin=20 * mm
        )
        styles = self.styles
        story = []

        ranked_articles = sorted(articles, key=self._priority_score, reverse=True)

        # --------------------------------
        # Title
        # --------------------------------
        story.append(Paragraph("China Battery Technology Intelligence Report", styles["Title"]))
        story.append(Paragraph("Generated: " + datetime.now().strftime("%Y-%m-%d"), styles["Normal"]))
        story.append(Spacer(1, 16))

        # --------------------------------
        # 1. Executive Synthesis
        # --------------------------------
        story.append(Paragraph("1. Executive Synthesis", styles["Heading2"]))

        top_articles = ranked_articles[:5]
        if top_articles:
            for article in top_articles:
                facts = article.get("facts", {})
                title = article.get("title", "No title")
                importance = facts.get("importance", 0) or 0
                companies = ", ".join(facts.get("companies", [])) or "\u2014"
                implication = facts.get("investment_implication") or "No implication extracted."

                block = (
                    f"<b>{title}</b><br/>"
                    f"Companies: {companies} | Importance: {importance}/5 "
                    f"({IMPORTANCE_LABELS.get(importance, 'UNRATED')})<br/>"
                    f"<i>{implication}</i>"
                )
                story.append(Paragraph(block, styles["Normal"]))

                for kf in facts.get("key_facts", [])[:3]:
                    story.append(Paragraph(f"\u2022 {kf}", styles["FactLabel"]))

                story.append(Spacer(1, 10))
        else:
            story.append(Paragraph("No articles available this period.", styles["Normal"]))

        story.append(PageBreak())

        # --------------------------------
        # 2. Technology Radar by Track
        # --------------------------------
        story.append(Paragraph("2. Technology Radar by Track", styles["Heading2"]))

        track_map = {}
        for article in articles:
            track_map.setdefault(self._track_for(article), []).append(article)

        track_order = list(TRACKS.keys()) + [OTHER_TRACK]
        for track in track_order:
            items = track_map.get(track, [])
            if not items:
                continue

            story.append(Paragraph(track, styles["TrackHeader"]))
            story.append(Paragraph(f"{len(items)} articles this period", styles["Normal"]))

            all_companies = set()
            all_events = []
            for item in items:
                facts = item.get("facts", {})
                all_companies.update(facts.get("companies", []))
                if facts.get("event_type"):
                    all_events.append(facts["event_type"])

            if all_companies:
                story.append(Paragraph(
                    "Companies mentioned: " + ", ".join(sorted(all_companies)),
                    styles["FactLabel"]
                ))
            if all_events:
                event_counts = Counter(all_events)
                event_str = ", ".join(f"{k} ({v})" for k, v in event_counts.most_common())
                story.append(Paragraph("Event types: " + event_str, styles["FactLabel"]))

            story.append(Spacer(1, 14))

        story.append(PageBreak())

        # --------------------------------
        # 3. Investment Priority Ranking
        # --------------------------------
        story.append(Paragraph("3. Investment Priority Ranking", styles["Heading2"]))

        for index, article in enumerate(ranked_articles, start=1):
            facts = article.get("facts", {})
            title = article.get("title", "")
            importance = facts.get("importance", 0) or 0
            label = IMPORTANCE_LABELS.get(importance, "UNRATED")

            text = (
                f"{index}. {title}<br/>"
                f"Importance: {importance}/5 ({label}) | "
                f"Keyword Score: {article.get('investment_score', 0)}/100"
            )
            story.append(Paragraph(text, styles["Normal"]))
            story.append(Spacer(1, 8))

        story.append(PageBreak())

        # --------------------------------
        # 4. Detailed Article Analysis
        # --------------------------------
        story.append(Paragraph("4. Detailed Article Analysis", styles["Heading2"]))

        for article in articles:
            facts = article.get("facts", {})
            title = article.get("title", "No title")
            source = article.get("source", "")
            link = article.get("link", "")

            story.append(Paragraph(title, styles["Heading3"]))
            story.append(Paragraph(f"Source: {source}", styles["FactLabel"]))
            if link:
                story.append(Paragraph(f"Link: {link}", styles["FactLabel"]))

            meta_rows = [
                ["Companies", ", ".join(facts.get("companies", [])) or "\u2014"],
                ["Technologies", ", ".join(facts.get("technologies", [])) or "\u2014"],
                ["Materials", ", ".join(facts.get("materials", [])) or "\u2014"],
                ["Event Type", facts.get("event_type") or "\u2014"],
                ["Capacity", facts.get("capacity") or "\u2014"],
                ["Energy Density", facts.get("energy_density") or "\u2014"],
                ["Investment Amount", facts.get("investment_amount") or "\u2014"],
                ["Timeframe", facts.get("timeframe") or "\u2014"],
            ]
            table = Table(meta_rows, colWidths=[110, 350])
            table.setStyle(TableStyle([
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#555555")),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
            ]))
            story.append(table)
            story.append(Spacer(1, 6))

            key_facts = facts.get("key_facts", [])
            if key_facts:
                story.append(Paragraph("Key Facts:", styles["FactLabel"]))
                for kf in key_facts:
                    story.append(Paragraph(f"\u2022 {kf}", styles["ArticleBody"]))

            implication = facts.get("investment_implication")
            if implication:
                story.append(Paragraph(
                    f"<b>Investment Implication:</b> {implication}", styles["ArticleBody"]
                ))

            story.append(Spacer(1, 18))
            story.append(HRFlowable(width="100%", color=colors.HexColor("#DDDDDD")))
            story.append(Spacer(1, 10))

        document.build(story)
        return filepath
