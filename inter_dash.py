import pandas as pd
import plotly.graph_objects as go
import vizro.plotly.express as px

import vizro.models as vm
from vizro import Vizro
from vizro.models.types import capture

df = pd.read_csv('number-of-deaths-by-risk-factor.csv')
df['Year'] = pd.to_datetime(df['Year'], format='%Y')


filters = [
    vm.Filter(column="Entity", selector=vm.Dropdown(title="Country")),
    vm.Filter(column="Year", selector=vm.DatePicker(range=True))
]

components = list()

for col in df.columns[3:7]:
    fig_col = px.scatter(df, x="Year", y=col, 
                        color="Entity", title=col.replace('Deaths that are from all causes attributed to ', '').title(), 
                        labels={"Year": "", col: ""}
                        )
    components.append(vm.Graph(figure=fig_col))

page_0 = vm.Page(
    title="Health-Related Deaths Dashboard",
    layout=vm.Layout(grid=[[0, 1],
                            [2, 3]]),
    components=components,
    controls=filters,
)

@capture("graph")
def stacked_bar(data_frame):
    values_to_remove = ['G20', 'World', '(WHO)', '(WB)']
    data_frame = data_frame[~data_frame['Entity'].str.contains('|'.join(values_to_remove))]
    
    data_frame = data_frame.drop(columns=["Entity", "Code"])
    df_agg = data_frame.groupby('Year').sum().reset_index()
    df_agg.columns = df_agg.columns.str.replace('Deaths that are from all causes attributed to ', '')
    df_agg.columns = df_agg.columns.str.split(',').str[0]

    # Sort the columns by the sum of values in descending order excluding 'Year' column
    sorted_cols = df_agg.drop(columns=['Year']).sum().sort_values(ascending=False).index
    df_agg = df_agg[['Year'] + sorted_cols.tolist()]

    # Combine the lowest 5 causes into 'Others'
    if len(df_agg.columns) > 6:  # Ensure there are more than 6 columns
        others_sum = df_agg.iloc[:, -8:].sum(axis=1)
        df_agg = pd.concat([df_agg.iloc[:, :-8], pd.DataFrame({'Others': others_sum})], axis=1)

    # Create the stacked bar chart
    fig = go.Figure()

    for i, col in enumerate(df_agg.columns[1:]):  # Exclude 'Year' column
        fig.add_trace(go.Bar(
            x=df_agg['Year'],
            y=df_agg[col],
            name=col,
        ))

    # Update layout
    fig.update_layout(
        title='Stacked Bar Chart of Causes of Death (Worldwide)',
        xaxis_title='Year',
        yaxis_title='Death Count',
        barmode='stack'  # Stacked bar chart
    )

    return fig

filters_2 = [
    vm.Filter(column="Entity", selector=vm.Dropdown(title="Country")),
    vm.Filter(column="Year", selector=vm.DatePicker(range=True))
]

page_1 = vm.Page(
    title="Custom Year on Year Deaths bar chart",
    path="my-custom-url",
    components=[
        vm.Graph(
            figure=stacked_bar(data_frame=df),
        ),
    ],
    controls=filters_2,
)
dashboard = vm.Dashboard(pages=[page_0,page_1])

Vizro().build(dashboard).run()
