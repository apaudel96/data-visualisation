from itertools import groupby
from numpy import size
import panel as pn
import pandas as pd

# import matplotlib.pyplot as plt
# import seaborn as sns
import plotly.express as px

pn.extension(sizing_mode="stretch_width")
# sns.set()

template = pn.template.FastListTemplate(
    title="Simple Sales Dashboard",
)

#####################################################
####################UTILITIES########################
#####################################################

_list_of_months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]


df = pd.read_excel("data/simple_sales.xlsx", sheet_name="Sales Data")

#####################################################
####################SIDEBAR##########################
#####################################################

# product category selector

category_selector_control = pn.widgets.Select(
    name="Category:",
    options=["All"] + df["Product Category"].sort_values().unique().tolist(),
    value="All",
)

# order by buttons
order_by_control = pn.widgets.RadioButtonGroup(
    name="Order By",
    options=["Index", "Sales", "Profit"],
    value="Index",
)

# ascending
ascending_control = pn.widgets.Toggle(name="Ascending", value=False)

template.sidebar.append(category_selector_control)
template.sidebar.append("Order By:")
template.sidebar.append(order_by_control)
template.sidebar.append("Toggle:")
template.sidebar.append(ascending_control)


#####################################################
###################GROUPED TABLES####################
#####################################################


# create a df of sales and profit, grouped by month
@pn.depends(
    category=category_selector_control,
    order_by=order_by_control,
    asc=ascending_control,
    # watch=True,
)
def month_df(category: str, order_by: str, asc):
    # copy of data
    df2 = df.copy()
    # filter by category
    if category != "All":
        df2 = df2[df2["Product Category"] == category]
    # select sales, profit, month
    df2 = df2[["Sales", "Profit", "Months"]]
    # make month categorical, sortable by _list_of_months
    df2["Months"] = pd.Categorical(
        df2["Months"], categories=_list_of_months, ordered=True
    )

    # group by month
    df2 = df2.groupby("Months").sum()

    # order by
    if order_by == "Index":
        df2 = df2.sort_index(ascending=asc)
    else:
        df2 = df2.sort_values(by=order_by, ascending=asc)

    # change profit to int
    df2["Profit"] = df2["Profit"].astype(int)
    # format sales, profit to 3sf
    df2["Sales"] = df2["Sales"].map("{:,.0f}".format)
    df2["Profit"] = df2["Profit"].map("{:,.0f}".format)
    # return df2
    return df2


# df of sales and profit, grouped by region
@pn.depends(
    category=category_selector_control, order_by=order_by_control, asc=ascending_control
)
def region_df(category: str, order_by: str, asc: bool):
    # copy of data
    df2 = df.copy()
    # filter by category
    if category != "All":
        df2 = df2[df2["Product Category"] == category]

    # select sales, profit, region
    df2 = df2[["Sales", "Profit", "Region"]]
    # group by region
    df2 = df2.groupby("Region").sum()

    # order by
    if order_by == "Index":
        df2 = df2.sort_index(ascending=asc)
    else:
        df2 = df2.sort_values(by=order_by, ascending=asc)

    # change profit to int
    df2["Profit"] = df2["Profit"].astype(int)
    # format sales, profit to 3sf
    df2["Sales"] = df2["Sales"].map("{:,.0f}".format)
    df2["Profit"] = df2["Profit"].map("{:,.0f}".format)
    # return df2
    return df2


template.main.append(
    pn.Row(
        pn.Column("#Sales and Profit by Month", month_df),
        pn.Column("#Sales and Profit by Region", region_df),
    )
)

#####################################################
####################Bar Charts#######################
#####################################################


@pn.depends(
    category=category_selector_control, order_by=order_by_control, asc=ascending_control
)
def month_bar_chart(category, order_by, asc):
    df2 = month_df(category, order_by, asc).reset_index()
    # convert sales and profit to int
    df2["Sales"] = df2["Sales"].str.replace(",", "").astype(int)
    df2["Profit"] = df2["Profit"].str.replace(",", "").astype(int)

    # stacked bar chart using plotly
    fig = px.bar(
        df2,
        x="Months",
        y=["Sales", "Profit"],
        template="seaborn",
    )
    return fig


@pn.depends(
    category=category_selector_control, order_by=order_by_control, asc=ascending_control
)
def region_bar_chart(category: str, order_by: str, asc: bool):
    df2 = region_df(category, order_by, asc).reset_index()
    # convert sales and profit to int
    df2["Sales"] = df2["Sales"].str.replace(",", "").astype(int)
    df2["Profit"] = df2["Profit"].str.replace(",", "").astype(int)

    # stacked bar chart using plotly
    fig = px.bar(
        df2,
        x="Region",
        y=["Sales", "Profit"],
        template="seaborn",
    )
    return fig


template.main.append(
    pn.Row(
        month_bar_chart,
        region_bar_chart,
    )
)


#####################################################
#####################################################
#####################################################


template.servable()
