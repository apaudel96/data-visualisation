import panel as pn
import pandas as pd
import plotly.express as px
import humanize

pn.extension("plotly", sizing_mode="stretch_width")

df = pd.read_csv("data/sales.csv")
df["Date"] = pd.to_datetime(df["Date"])
df["Sales"] = df["Quantity"] * df["Price"]

df["CustomerNo"] = df["CustomerNo"].apply(lambda x: "" if pd.isnull(x) else f"{x:.0f}")


def data_table():
    return pn.Column(
        "<h1 align=center>Data</h1>",
        "---",
        df.head(5),
    )


def kpi():
    sum_sales = df["Sales"].sum()
    avg_sales = df["Sales"].mean()
    sum_num_items = df["Quantity"].sum()

    return pn.Column(
        "<h1 align=center>KPIs</h1>",
        pn.Row(
            pn.Column(
                pn.pane.Markdown(
                    f"<h2 align=center>{humanize.intword(sum_sales)}</h2>"
                ),
                pn.pane.Markdown("<p align=center>Total Sales</p>"),
            ),
            pn.Column(
                pn.pane.Markdown(
                    f"<h2 align=center>{humanize.intword(avg_sales)}</h2>"
                ),
                pn.pane.Markdown("<p align=center>Average amount per transaction</p>"),
            ),
            pn.Column(
                pn.pane.Markdown(
                    f"<h2 align=center>{humanize.intword(sum_num_items)}</h2>"
                ),
                pn.pane.Markdown("<p align=center>Total products sold</p>"),
            ),
        ),
        # width=600,
        # sizing_mode="stretch_height",
    )


def sales_by_time_line():
    df2 = df[["Date", "Sales"]].copy()
    df2 = df2.groupby("Date").sum().reset_index()
    fig = px.line(
        df2,
        x="Date",
        y="Sales",
        template="seaborn"
        # width=1600,
    )
    fig.update_layout(hovermode="x unified")
    return pn.Column(
        "<h1 align=center>Total sales over time</h1>",
        # pn.pane.Plotly(fig),
        fig,
    )


def country_sales_map():
    def create_graph(date):
        parsed_date = pd.Timestamp(date)
        df2 = df[["Country", "Sales", "Date"]].copy()
        df2 = df2.query("Date == @date")
        df2 = df2.groupby(["Country"]).sum().reset_index()
        fig = px.choropleth(
            df2,
            color="Sales",
            locations="Country",
            locationmode="country names",
            height=800,
            template="seaborn",
        )
        return fig

    # date_slider = pn.widgets.DiscreteSlider(name="Date", options = {pd.to_datetime(number):number for number in df["Date"].sort_values().unique().tolist()})
    date_slider = pn.widgets.DateSlider(
        name="Date",
        start=df["Date"].min().date(),
        end=df["Date"].max().date(),
        value=df["Date"].min().date(),
    )

    return pn.Column(
        "#Sales by country for given year",
        date_slider,
        pn.bind(create_graph, date_slider),
    )


def product_by_sales():
    def create_graph(limit: int, ascending: bool):
        df2 = (
            df[["ProductName", "Sales"]]
            .copy()
            .groupby("ProductName")
            .sum()
            .reset_index()
        )
        df2 = df2.sort_values("Sales", ascending=ascending).head(limit)
        fig = px.bar(
            df2,
            x="ProductName",
            y="Sales",
            template="seaborn",
        )
        return fig

    limit_product = pn.widgets.IntSlider(name="Limit", value=10, start=5, end=50)
    ascending_product = pn.widgets.Checkbox(name="Ascending", value=False)
    return pn.Column(
        "#Product by sales",
        limit_product,
        ascending_product,
        pn.bind(create_graph, limit=limit_product, ascending=ascending_product),
    )


def customer_by_sales():
    def create_graph(limit: int, ascending: bool):
        df2 = (
            df[["CustomerNo", "Sales"]].copy().groupby("CustomerNo").sum().reset_index()
        )
        df2 = df2.sort_values("Sales", ascending=ascending).head(limit)
        fig = px.bar(
            df2,
            x="CustomerNo",
            y="Sales",
            template="seaborn",
        )
        return fig

    limit_customer = pn.widgets.IntSlider(name="Limit", value=10, start=5, end=50)
    ascending_customer = pn.widgets.Checkbox(name="Ascending", value=False)
    return pn.Column(
        "#Customer by sales",
        limit_customer,
        ascending_customer,
        pn.bind(create_graph, limit_customer, ascending_customer),
    )


# template = pn.template.FastListTemplate(title="Sales Dashboard")

# template.main.append(data_table())
# template.main.append(
#     pn.Row(
#         kpi(),
#         sales_by_time_line(),
#     )
# )
# template.main.append(sales_by_time_line())

# template = pn.template.FastGridTemplate(title="Sales Dashboard")
template = pn.template.FastGridTemplate(title="Sales Dashboard")
template.main[0:2, 0:4] = kpi()
template.main[0:4, 4:12] = sales_by_time_line()

template.main[4:10, 4:12] = country_sales_map()
template.main[2:6, 0:4] = product_by_sales()
template.main[6:10, 0:4] = customer_by_sales()

template.servable()
