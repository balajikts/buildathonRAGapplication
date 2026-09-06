from pathlib import Path

import pandas as pd
import streamlit as st


EXCEL_FILE = Path(
    "output/rag_results.xlsx"
)


def load_rag_results():

    if not EXCEL_FILE.exists():

        return pd.DataFrame()

    try:

        return pd.read_excel(
            EXCEL_FILE
        )

    except Exception as error:

        st.error(
            f"Unable to read Excel file: {error}"
        )

        return pd.DataFrame()


def show_dashboard():

    st.title("📊 RAG Metrics Dashboard")

    df = load_rag_results()

    if df.empty:

        st.info(
            "No RAG execution data is available yet."
        )

        return


    # ------------------------------------------
    # CLEAN DATA
    # ------------------------------------------

    df["Status"] = (
        df["Status"]
        .astype(str)
        .str.upper()
    )


    # ------------------------------------------
    # METRICS
    # ------------------------------------------

    total_queries = len(df)

    success_count = len(
        df[df["Status"] == "SUCCESS"]
    )

    not_found_count = len(
        df[df["Status"] == "NOT_FOUND"]
    )

    failed_count = len(
        df[df["Status"] == "FAILED"]
    )


    if total_queries > 0:

        success_rate = (
            success_count
            / total_queries
        ) * 100

    else:

        success_rate = 0


    if "Latency Seconds" in df.columns:

        average_latency = pd.to_numeric(
            df["Latency Seconds"],
            errors="coerce"
        ).mean()

    else:

        average_latency = 0


    # ------------------------------------------
    # KPI CARDS
    # ------------------------------------------

    col1, col2, col3, col4, col5 = st.columns(5)


    col1.metric(
        "Total Queries",
        total_queries
    )

    col2.metric(
        "Successful",
        success_count
    )

    col3.metric(
        "Not Found",
        not_found_count
    )

    col4.metric(
        "Failed",
        failed_count
    )

    col5.metric(
        "Success Rate",
        f"{success_rate:.1f}%"
    )


    st.divider()


    # ------------------------------------------
    # PERFORMANCE
    # ------------------------------------------

    st.subheader(
        "⚡ Performance"
    )

    st.metric(
        "Average Response Time",
        f"{average_latency:.2f} seconds"
    )


    st.divider()


    # ------------------------------------------
    # STATUS DISTRIBUTION
    # ------------------------------------------

    st.subheader(
        "📈 Response Status Distribution"
    )

    status_counts = (
        df["Status"]
        .value_counts()
    )

    st.bar_chart(
        status_counts
    )


    st.divider()


    # ------------------------------------------
    # SOURCE DISTRIBUTION
    # ------------------------------------------

    st.subheader(
        "📚 Source Distribution"
    )

    if "Categories" in df.columns:

        categories = (
            df["Categories"]
            .fillna("Unknown")
            .astype(str)
            .str.split(", ")
            .explode()
            .value_counts()
        )

        st.bar_chart(
            categories
        )


    st.divider()


    # ------------------------------------------
    # RECENT QUERIES
    # ------------------------------------------

    st.subheader(
        "🕐 Recent Queries"
    )

    recent_columns = [
        "Timestamp",
        "User Input",
        "Status",
        "Latency Seconds"
    ]

    available_columns = [
        column
        for column in recent_columns
        if column in df.columns
    ]

    recent_df = (
        df[available_columns]
        .tail(10)
        .iloc[::-1]
    )

    st.dataframe(
        recent_df,
        width="stretch",
        hide_index=True
    )


    st.divider()


    # ------------------------------------------
    # FULL EXECUTION LOG
    # ------------------------------------------

    with st.expander(
        "📋 View Complete RAG Execution Log"
    ):

        st.dataframe(
            df,
            width="stretch",
            hide_index=True
        )