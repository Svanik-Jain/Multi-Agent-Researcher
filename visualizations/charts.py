
import html
import math
import streamlit as st


# ==================================================
# 1. HELPER FUNCTIONS
# ==================================================

def to_number(value):
    """Convert numeric values and numeric strings to float."""

    if isinstance(value, bool) or value is None:
        return None

    try:
        number = float(
            str(value)
            .replace(",", "")
            .replace("%", "")
            .strip()
        )

        if not math.isfinite(number):
            return None

        return number

    except (ValueError, TypeError):
        return None


def safe_text(value):
    """Escape text before inserting it into SVG."""

    return html.escape(str(value if value is not None else ""))


def format_number(value):
    """Format a number without unnecessary decimal places."""

    number = to_number(value)

    if number is None:
        return str(value)

    return f"{number:,.2f}".rstrip("0").rstrip(".")


# ==================================================
# 2. SOURCE LINKS
# ==================================================

def display_sources(items):

    sources = []

    for item in items:

        url = item.get("source_url")

        if url:
            sources.append(item)

    if not sources:
        return

    with st.expander("View metric sources"):

        for source in sources:

            name = source.get("name", "Source")
            source_id = source.get("source_id")
            url = source.get("source_url")

            label = name

            if source_id:
                label += f" ({source_id})"

            st.markdown(
                f"- **{safe_text(label)}**: [Open source]({url})"
            )


# ==================================================
# 3. BAR CHART
# ==================================================

def create_bar_chart(items, title, unit=""):

    valid_items = []

    for item in items:

        value = to_number(item.get("value"))

        if value is not None:

            valid_items.append({
                **item,
                "_numeric_value": value
            })

    if not valid_items:

        st.warning(f"No numerical data available for {title}.")
        return

    # Chart dimensions
    width = 1150
    label_width = 430
    chart_width = 460
    value_x = label_width + chart_width + 20

    bar_height = 30
    gap = 75
    top_padding = 65
    bottom_padding = 35

    height = top_padding + len(valid_items) * gap + bottom_padding

    max_value = max(
        abs(item["_numeric_value"])
        for item in valid_items
    )

    if max_value == 0:
        max_value = 1

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {width} {height}" '
        f'width="100%" height="{height}" '
        f'style="display:block;">',

        """
        <style>
            .chart-title {
                font-size: 23px;
                font-weight: bold;
                fill: #333333;
            }

            .chart-label {
                font-size: 16px;
                fill: #333333;
            }

            .chart-value {
                font-size: 16px;
                font-weight: bold;
                fill: #333333;
            }
        </style>
        """,

        f'<text x="5" y="32" class="chart-title">'
        f'{safe_text(title)}</text>'
    ]

    for index, item in enumerate(valid_items):

        name = str(item.get("name", "Unnamed metric"))
        value = item["_numeric_value"]

        y = top_padding + index * gap

        # ------------------------------------------
        # WRAP LABEL INTO MULTIPLE LINES
        # ------------------------------------------

        words = name.split()
        lines = []
        current_line = ""

        max_characters = 40

        for word in words:

            test_line = (
                current_line + " " + word
                if current_line
                else word
            )

            if len(test_line) > max_characters:

                if current_line:
                    lines.append(current_line)

                current_line = word

            else:
                current_line = test_line

        if current_line:
            lines.append(current_line)

        # Maximum two lines
        if len(lines) > 2:
            lines = lines[:2]
            lines[1] = lines[1].rstrip(" .") + "..."

        # ------------------------------------------
        # DRAW LABEL
        # ------------------------------------------

        for line_index, line in enumerate(lines):

            label_y = y + 11 + line_index * 20

            svg.append(
                f'<text x="5" y="{label_y}" '
                f'class="chart-label">'
                f'{safe_text(line)}'
                f'</text>'
            )

        # ------------------------------------------
        # DRAW BAR
        # ------------------------------------------

        bar_width = (
            abs(value) / max_value
        ) * chart_width

        svg.append(
            f'<rect '
            f'x="{label_width}" '
            f'y="{y}" '
            f'width="{bar_width}" '
            f'height="{bar_height}" '
            f'rx="5" '
            f'fill="#4F81BD"/>'
        )

        # ------------------------------------------
        # DRAW VALUE
        # ------------------------------------------

        display_value = format_number(value)

        svg.append(
            f'<text '
            f'x="{value_x}" '
            f'y="{y + 21}" '
            f'class="chart-value">'
            f'{safe_text(display_value)} {safe_text(unit)}'
            f'</text>'
        )

    svg.append("</svg>")

    # Render SVG in a dedicated HTML component
    st.components.v1.html(
        "".join(svg),
        height=height + 30,
        scrolling=False
    )


# ==================================================
# 4. LINE CHART
# ==================================================

def create_line_chart(series):

    if not series:
        return

    title = series.get("title", "Trend Over Time")

    periods = series.get(
        "periods",
        series.get("labels", [])
    )

    values = series.get("values", [])

    if not periods or not values:
        return

    valid_data = []

    for period, value in zip(periods, values):

        number = to_number(value)

        if number is not None:
            valid_data.append((str(period), number))

    if len(valid_data) < 2:

        st.info(f"Not enough data to plot {title}.")
        return

    width = 950
    height = 420

    left = 80
    right = 40
    top = 65
    bottom = 80

    chart_width = width - left - right
    chart_height = height - top - bottom

    numbers = [value for _, value in valid_data]

    min_value = min(numbers)
    max_value = max(numbers)

    value_range = max_value - min_value

    if value_range == 0:
        value_range = max(abs(max_value), 1)

    min_value -= value_range * 0.1
    max_value += value_range * 0.1

    adjusted_range = max_value - min_value

    def x_position(index):

        return (
            left
            + index * chart_width / (len(valid_data) - 1)
        )

    def y_position(value):

        return (
            top
            + chart_height
            - (
                (value - min_value)
                / adjusted_range
            ) * chart_height
        )

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {width} {height}" '
        f'width="100%" height="auto" '
        f'style="display:block;">',

        """
        <style>
            .line-title {
                font-size: 23px;
                font-weight: bold;
                fill: #333333;
            }

            .axis-label {
                font-size: 13px;
                fill: #666666;
            }

            .point-label {
                font-size: 13px;
                font-weight: bold;
                fill: #333333;
            }
        </style>
        """,

        f'<text x="{left}" y="30" class="line-title">'
        f'{safe_text(title)}</text>'
    ]

    # Grid lines and Y-axis labels
    for i in range(5):

        value = min_value + adjusted_range * i / 4

        y = top + chart_height - i * chart_height / 4

        svg.append(
            f'<line x1="{left}" y1="{y}" '
            f'x2="{width - right}" y2="{y}" '
            f'stroke="#dddddd" stroke-width="1"/>'
        )

        svg.append(
            f'<text x="{left - 12}" y="{y + 5}" '
            f'text-anchor="end" class="axis-label">'
            f'{format_number(value)}'
            f'</text>'
        )

    # X-axis labels
    for index, (period, value) in enumerate(valid_data):

        x = x_position(index)

        svg.append(
            f'<text x="{x}" y="{height - 35}" '
            f'text-anchor="middle" class="axis-label">'
            f'{safe_text(period)}'
            f'</text>'
        )

    # Line points
    points = []

    for index, (period, value) in enumerate(valid_data):

        x = x_position(index)
        y = y_position(value)

        points.append(f"{x},{y}")

    svg.append(
        f'<polyline points="{" ".join(points)}" '
        f'fill="none" stroke="#4F81BD" '
        f'stroke-width="3" stroke-linejoin="round"/>'
    )

    # Circles and value labels
    for index, (period, value) in enumerate(valid_data):

        x = x_position(index)
        y = y_position(value)

        svg.append(
            f'<circle cx="{x}" cy="{y}" r="5" '
            f'fill="#4F81BD"/>'
        )

        svg.append(
            f'<text x="{x}" y="{y - 12}" '
            f'text-anchor="middle" class="point-label">'
            f'{format_number(value)}'
            f'</text>'
        )

    svg.append("</svg>")

    st.components.v1.html(
        "".join(svg),
        height=height + 20,
        scrolling=False
    )


# ==================================================
# 5. KEY METRIC CARDS
# ==================================================

def display_key_metrics(metrics):

    if not metrics:
        return

    st.subheader("Key Metrics")

    columns = st.columns(4)

    for index, metric in enumerate(metrics):

        name = metric.get("name", "Metric")
        value = metric.get("value", "N/A")
        unit = metric.get("unit", "")

        with columns[index % 4]:

            st.metric(
                label=name,
                value=f"{format_number(value)} {unit}"
            )

            context = metric.get("context")

            if context:
                st.caption(context)


# ==================================================
# 6. AUTOMATIC BAR CHART GENERATION
# ==================================================

def display_metric_charts(metrics):

    st.subheader("Automatic Metric Charts")

    grouped_metrics = {}

    for metric in metrics:

        unit = str(
            metric.get("unit", "Other")
        ).strip().lower()

        value = to_number(metric.get("value"))

        if value is None:
            continue

        grouped_metrics.setdefault(unit, []).append(metric)

    charts_created = 0

    for unit, items in grouped_metrics.items():

        if len(items) >= 2:

            st.markdown(f"#### Metrics measured in {unit}")

            create_bar_chart(
                items,
                title=f"Different {unit}-based metrics",
                unit=unit
            )

            st.caption(
                "These metrics share a unit but measure different "
                "things. They are not necessarily directly comparable."
            )

            charts_created += 1

    if charts_created == 0:

        st.warning(
            "No groups with at least two numerical metrics "
            "were found. Showing available metrics below."
        )

        for metric in metrics:

            st.write(
                metric.get("name"),
                metric.get("value"),
                metric.get("unit")
            )


# ==================================================
# 7. OPPORTUNITIES AND RISKS
# ==================================================

def display_strategy_insights(opportunities, risks):

    if not opportunities and not risks:
        return

    st.subheader("Strategic Insights")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### Opportunities")

        if opportunities:

            for opportunity in opportunities:

                with st.container(border=True):

                    st.markdown(
                        f"**{opportunity.get('title', 'Opportunity')}**"
                    )

                    st.write(
                        opportunity.get("description", "")
                    )

        else:
            st.info("No opportunities identified.")

    with col2:

        st.markdown("### Risks")

        if risks:

            for risk in risks:

                with st.container(border=True):

                    st.markdown(
                        f"**{risk.get('title', 'Risk')}**"
                    )

                    st.write(
                        risk.get("description", "")
                    )

        else:
            st.info("No risks identified.")


# ==================================================
# 8. MAIN VISUALIZATION FUNCTION
# ==================================================

def display_visualizations(data):

    if not isinstance(data, dict) or not data:

        st.info("No visual data available.")
        return

    metrics = data.get("key_metrics", [])
    time_series = data.get("time_series", [])
    comparisons = data.get("comparisons", [])
    opportunities = data.get("opportunities", [])
    risks = data.get("risks", [])

    # ----------------------------------------------
    # KEY METRICS
    # ----------------------------------------------

    if metrics:

        display_key_metrics(metrics)

        st.divider()

    # ----------------------------------------------
    # AUTOMATIC CHARTS FROM METRICS
    # Always attempt this independently.
    # ----------------------------------------------

    if metrics:

        display_metric_charts(metrics)

        st.divider()

    # ----------------------------------------------
    # TIME SERIES
    # ----------------------------------------------

    if time_series:

        st.subheader("Trends Over Time")

        for series in time_series:

            create_line_chart(series)

        st.divider()

    # ----------------------------------------------
    # EXPLICIT COMPARISONS
    # ----------------------------------------------

    if comparisons:

        st.subheader("Comparisons")

        for comparison in comparisons:

            title = comparison.get(
                "title",
                "Comparison"
            )

            items = comparison.get(
                "items",
                comparison.get("data", [])
            )

            unit = comparison.get("unit", "")

            create_bar_chart(
                items,
                title=title,
                unit=unit
            )

        st.divider()

    # ----------------------------------------------
    # SOURCES
    # ----------------------------------------------

    if metrics:

        display_sources(metrics)

    # ----------------------------------------------
    # OPPORTUNITIES AND RISKS
    # ----------------------------------------------

    if opportunities or risks:

        display_strategy_insights(
            opportunities,
            risks
        )
