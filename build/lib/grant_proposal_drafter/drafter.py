import string


DISCLAIMER = (
    "This document is an AI-generated educational draft only. It is not legal, "
    "financial, medical, or professional grant-writing advice, and it does not "
    "create any professional relationship. Asdale Dynamics, LLC makes no "
    "representations or warranties about its accuracy, completeness, or "
    "suitability for any particular grant program. Review all generated content "
    "with qualified professionals before submission to any funder. Asdale "
    "Dynamics, LLC is not responsible for outcomes from use of this draft."
)

SECTION_ORDER = [
    "executive_summary",
    "statement_of_need",
    "project_description",
    "goals_and_objectives",
    "budget_narrative",
    "evaluation_plan",
    "sustainability_plan",
    "conclusion",
]

SECTION_TITLES = {
    "executive_summary": "Executive Summary",
    "statement_of_need": "Statement of Need",
    "project_description": "Project Description",
    "goals_and_objectives": "Goals and Objectives",
    "budget_narrative": "Budget Narrative",
    "evaluation_plan": "Evaluation Plan",
    "sustainability_plan": "Sustainability Plan",
    "conclusion": "Conclusion",
}

SYSTEM_PROMPT = (
    "You are a helpful assistant that drafts grant proposal sections for "
    "educational purposes only. Output only the requested section in Markdown. "
    "Do not provide legal, financial, or medical advice. Do not invent "
    "specific funder names, award dates, or guarantees of funding."
)

_PROMPTS = {
    "executive_summary": (
        "Draft an Executive Summary for a grant proposal using these project details:\n"
        "- Title: $title\n"
        "- Organization: $organization\n"
        "- Requested amount: $amount\n"
        "- Duration: $duration\n"
        "- Target population: $target_population\n"
        "- Problem statement: $problem_statement\n"
        "- Goals: $goals\n"
        "- Activities: $activities\n\n"
        "Write a concise, compelling executive summary (about one page) in "
        "Markdown. Include the amount requested and what the project will "
        "achieve. Education-only draft; not legal or financial advice."
    ),
    "statement_of_need": (
        "Draft a Statement of Need for a grant proposal using these project "
        "details:\n"
        "- Title: $title\n"
        "- Organization: $organization\n"
        "- Target population: $target_population\n"
        "- Problem statement: $problem_statement\n\n"
        "Explain why the project matters, who it serves, and what happens if "
        "it is not funded. Use plain, compassionate language. Education-only "
        "draft."
    ),
    "project_description": (
        "Draft a Project Description for a grant proposal using these project "
        "details:\n"
        "- Title: $title\n"
        "- Organization: $organization\n"
        "- Duration: $duration\n"
        "- Activities: $activities\n"
        "- Goals: $goals\n\n"
        "Describe what the project will do, how it will be carried out, who "
        "will carry it out, and the timeline. Education-only draft."
    ),
    "goals_and_objectives": (
        "Draft Goals and Objectives for a grant proposal using these project "
        "details:\n"
        "- Title: $title\n"
        "- Goals: $goals\n"
        "- Activities: $activities\n"
        "- Duration: $duration\n\n"
        "State clear goals and measurable, specific objectives. Education-only "
        "draft."
    ),
    "budget_narrative": (
        "Draft a Budget Narrative for a grant proposal using these project "
        "details:\n"
        "- Title: $title\n"
        "- Requested amount: $amount\n"
        "- Duration: $duration\n"
        "- Budget items: $budget_items\n\n"
        "Explain how the requested funds will be spent and why each cost is "
        "necessary. Education-only draft; not financial advice."
    ),
    "evaluation_plan": (
        "Draft an Evaluation Plan for a grant proposal using these project "
        "details:\n"
        "- Title: $title\n"
        "- Goals: $goals\n"
        "- Evaluation metrics: $evaluation_metrics\n\n"
        "Describe how success will be measured and reported. Education-only "
        "draft."
    ),
    "sustainability_plan": (
        "Draft a Sustainability Plan for a grant proposal using these project "
        "details:\n"
        "- Title: $title\n"
        "- Organization: $organization\n"
        "- Duration: $duration\n\n"
        "Explain how the project will continue after grant funding ends. "
        "Education-only draft."
    ),
    "conclusion": (
        "Draft a Conclusion for a grant proposal using these project details:\n"
        "- Title: $title\n"
        "- Organization: $organization\n"
        "- Requested amount: $amount\n"
        "- Goals: $goals\n\n"
        "Summarize the request and its expected impact in a short, grateful "
        "closing. Education-only draft."
    ),
}

DEFAULT_DETAILS = {
    "title": "Untitled Grant Proposal",
    "organization": "Applicant Organization",
    "amount": "not specified",
    "duration": "12 months",
    "contact": "not specified",
    "target_population": "the community served by the applicant",
    "problem_statement": "not provided",
    "goals": "not provided",
    "activities": "not provided",
    "budget_items": "not provided",
    "evaluation_metrics": "not provided",
    "sustainability": "not provided",
}


class GrantDrafter:
    def __init__(self, client):
        self.client = client

    def _fill(self, template, details):
        values = dict(DEFAULT_DETAILS)
        values.update(details or {})
        return string.Template(template).substitute(values)

    def draft_section(self, name, details):
        if name not in _PROMPTS:
            raise ValueError(f"Unknown section: {name}")
        user_prompt = self._fill(_PROMPTS[name], details)
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ]
        return self.client.chat(messages)

    def draft_all(self, details):
        return {name: self.draft_section(name, details) for name in SECTION_ORDER}

    def render_markdown(self, details, sections):
        values = dict(DEFAULT_DETAILS)
        values.update(details or {})
        lines = [f"# {values['title']}", ""]
        lines.append("Grant Proposal Draft - generated by grant-proposal-drafter (Asdale Dynamics, LLC)")
        lines.append("")
        lines.append("## Education-Only Disclaimer")
        lines.append("")
        lines.append(DISCLAIMER)
        lines.append("")
        lines.append(f"Organization: {values['organization']}")
        lines.append(f"Requested amount: {values['amount']}")
        lines.append(f"Duration: {values['duration']}")
        lines.append(f"Contact: {values['contact']}")
        lines.append("")
        for name in SECTION_ORDER:
            lines.append(f"## {SECTION_TITLES[name]}")
            lines.append("")
            lines.append(sections[name])
            lines.append("")
        lines.append("---")
        lines.append(
            "This draft was generated by an AI-assisted tool for educational "
            "purposes. Review it with qualified professionals before submitting "
            "to any funder. Asdale Dynamics, LLC."
        )
        return "\n".join(lines)
