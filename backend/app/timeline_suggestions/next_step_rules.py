def suggest_next_steps(timeline):
    """
    Generate rule-based next-step suggestions
    from the events present in a crime investigation timeline.
    """

    if not timeline:
        return []

    suggestions = []

    event_names = [
        event.get("event", "").lower()
        for event in timeline
    ]

    # Rule 1: Case has been created but no evidence has been collected
    if "case created" in event_names and "evidence collected" not in event_names:
        suggestions.append(
            "Collect and document available physical or digital evidence."
        )

    # Rule 2: Evidence collected but no forensic analysis
    if (
        "evidence collected" in event_names
        and "forensic analysis completed" not in event_names
    ):
        suggestions.append(
            "Perform forensic analysis on the collected evidence."
        )

    # Rule 3: Witness statement exists but no suspect interview
    if (
        "witness statement" in event_names
        and "suspect interview completed" not in event_names
    ):
        suggestions.append(
            "Conduct a suspect interview based on available witness information."
        )

    # Rule 4: Forensic analysis completed but no evidence report
    if (
        "forensic analysis completed" in event_names
        and "forensic report generated" not in event_names
    ):
        suggestions.append(
            "Generate and document the forensic analysis report."
        )

    # Rule 5: Evidence report exists but investigation has no conclusion
    if (
        "forensic report generated" in event_names
        and "investigation concluded" not in event_names
    ):
        suggestions.append(
            "Review all evidence and prepare the investigation conclusion."
        )

    return suggestions