import streamlit as st
import pandas as pd
from pathlib import Path

# пути к витринам
BASE_DIR = Path(__file__).parent
DATA_AGGR = BASE_DIR / "data" / "aggregated"

CITY_RATING_CSV = DATA_AGGR / "city_tourism_rating.csv"
FD_SUMMARY_CSV = DATA_AGGR / "federal_districts_summary.csv"
TRAVEL_RECO_CSV = DATA_AGGR / "travel_recommendations.csv"


@st.cache_data
def load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def show_city_rating():
    st.header("Витрина 1 — Рейтинг городов для туризма")

    df = load_csv(CITY_RATING_CSV)
    if df.empty:
        st.warning("Файл city_tourism_rating.csv не найден или пустой.")
        return

    st.subheader("Таблица рейтинга городов")
    st.dataframe(df)

    st.subheader("Средний индекс комфортности по городам")
    st.bar_chart(df.set_index("city_name")["comfort_index"])


def show_federal_summary():
    st.header("Витрина 2 — Сводка по федеральным округам")

    df = load_csv(FD_SUMMARY_CSV)
    if df.empty:
        st.warning("Файл federal_districts_summary.csv не найден или пустой.")
        return

    st.subheader("Таблица по округам")
    st.dataframe(df)

    st.subheader("Средняя температура по округам")
    st.bar_chart(df.set_index("federal_district")["temperature_max"])

    st.subheader("Средний индекс комфортности по округам")
    st.bar_chart(df.set_index("federal_district")["comfort_index"])


def show_travel_recommendations():
    st.header("Витрина 3 — Отчёт для турагентств")

    df = load_csv(TRAVEL_RECO_CSV)
    if df.empty:
        st.warning("Файл travel_recommendations.csv не найден или пустой.")
        return

    st.subheader("Рекомендации на текущую дату")
    st.dataframe(df)

    # простая текстовая выжимка
    go_cities = df[df.get("status", "Ехать") != "Лучше дома"]["city_name"].tolist()
    stay_cities = df[df.get("status", "Ехать") == "Лучше дома"]["city_name"].tolist()

    if go_cities:
        st.markdown("**Топ городов для поездки:** " + ", ".join(go_cities))
    if stay_cities:
        st.markdown("**Города, где лучше остаться дома:** " + ", ".join(stay_cities))


def main():
    st.title("Туристический погодный дэшборд")
    st.caption("Пайплайн: RAW → CLEANED → ENRICHED → AGGREGATED")

    page = st.sidebar.selectbox(
        "Выберите витрину",
        [
            "Рейтинг городов",
            "Сводка по федеральным округам",
            "Отчёт для турагентств",
        ],
    )

    if page == "Рейтинг городов":
        show_city_rating()
    elif page == "Сводка по федеральным округам":
        show_federal_summary()
    else:
        show_travel_recommendations()


if __name__ == "__main__":
    main()