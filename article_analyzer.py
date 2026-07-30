import os
import json
from openai import OpenAI


class ArticleAnalyzer:
    """
    Analyze battery industry articles and extract structured facts.
    """

    def __init__(self):

        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

    def analyze(self, article):

        title = article.get("title", "")
        content = article.get("content", "")

        if len(content) > 6000:
            content = content[:6000]

        prompt = f"""
You are a senior battery industry analyst.

Read the following article.

Extract only factual information.

Return JSON only.

Required JSON format:

{{
    "companies": [],
    "technologies": [],
    "materials": [],
    "countries": [],
    "event_type": "",
    "capacity": "",
    "energy_density": "",
    "production_scale": "",
    "investment_amount": "",
    "timeframe": "",
    "importance": 1,
    "key_facts": [],
    "investment_implication": ""
}}

Rules

- companies:
  CATL, BYD, EVE, CALB, Gotion, LG Energy Solution,
  Samsung SDI, SK On, Tesla, Panasonic...

- technologies:
  LFP
  LMFP
  LMR
  Sodium-ion
  Solid-state
  Semi-solid
  Silicon Anode
  Dry Electrode
  ESS

- event_type examples

Policy
Factory
Gigafactory
Mass Production
Partnership
Joint Venture
Investment
Technology Breakthrough
Product Launch
Research
Supply Chain

importance

1 = minor

2 = useful

3 = important

4 = major

5 = industry changing

Title:
{title}

Article:

{content}
"""

        response = self.client.chat.completions.create(

            model="gpt-5",

            messages=[
                {
                    "role": "system",
                    "content": "You extract structured battery industry facts."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0
        )

        result = response.choices[0].message.content

        try:
            return json.loads(result)

        except Exception:

            return {
                "companies": [],
                "technologies": [],
                "materials": [],
                "countries": [],
                "event_type": "",
                "capacity": "",
                "energy_density": "",
                "production_scale": "",
                "investment_amount": "",
                "timeframe": "",
                "importance": 1,
                "key_facts": [],
                "investment_implication": ""
            }
