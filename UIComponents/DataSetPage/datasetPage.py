import dash_bootstrap_components as dbc
import dash_html_components as html

from DataSetPage.components.dataSetCard import DataSetCard, AddDataSetCard
from DataSetPage.components.datasetNavBar import NavBar

DATASET_DIV_STYLE = {
    "margin-bottom": 100,
}
DATSET_DIV_TITLE = {
    "margin-bottom": 30
}


def DataSetPage():
    navbar = NavBar()

    call_datasets = dbc.Row(
        [

            DataSetCard(name="Call DataSet 1", records=12455, type="call"),
            DataSetCard(name="Call DataSet 2", records=24000, type="call"),
            AddDataSetCard(d_type="call"),
        ]
    )
    msg_datasets = dbc.Row(
        [
            DataSetCard(name="Message DataSet 1", records=9415, type="msg"),
            DataSetCard(name="Message DataSet 2", records=7300, type="msg"),
            DataSetCard(name="Message DataSet 3", records=1415, type="msg"),
            DataSetCard(name="Message DataSet 4", records=7510, type="msg"),
            AddDataSetCard(d_type="message"),
        ]
    )
    cell_datasets = dbc.Row(
        [
            DataSetCard(name="Cell DataSet 1", records=23, type="cell"),
            AddDataSetCard(d_type="cell"),
        ]
    )

    call_datasets_content = html.Div(
        children=[
            html.H2("Call DataSets", style=DATSET_DIV_TITLE),
            call_datasets,
        ],
        style=DATASET_DIV_STYLE
    )
    msg_datasets_content = html.Div(
        children=[
            html.H2("Message DataSets", style=DATSET_DIV_TITLE),
            msg_datasets,
        ],
        style=DATASET_DIV_STYLE
    )
    celll_datasets_content = html.Div(
        children=[
            html.H2("Cell/Antenna DataSets", style=DATSET_DIV_TITLE),
            cell_datasets,
        ],
        style=DATASET_DIV_STYLE
    )

    content = html.Div(
        children=[
            call_datasets_content,
            msg_datasets_content,
            celll_datasets_content,

        ],
        style={"margin": 20, "margin-top": 100}

    )

    return html.Div(children=[content, navbar])
