import pandas as pd
import vizro.plotly.express as px
import vizro.models as vm
from vizro import Vizro

# Load the data
df = pd.read_csv('number-of-deaths-by-risk-factor.csv')
df['Year'] = pd.to_datetime(df['Year'], format='%Y')

# Create a scatter plot for high systolic blood pressure deaths over years
fig_sbp = px.scatter(df, x="Year", y="Deaths that are from all causes attributed to high systolic blood pressure, in both sexes aged all ages", color="Entity", title="High Systolic Blood Pressure Deaths Over Years")

# Create a scatter plot for diet high in sodium deaths over years
fig_sodium = px.scatter(df, x="Year", y="Deaths that are from all causes attributed to diet high in sodium, in both sexes aged all ages", color="Entity", title="Diet High in Sodium Deaths Over Years")

# Add filters
filters = [
    vm.Filter(column="Entity", selector=vm.Dropdown(title="Country")),
    vm.Filter(column="Year", selector=vm.DatePicker(range=True))
]

# Create a page with the graphs and filters
temp_page = vm.Page(
    title="Temporary Dashboard",
    components=[
        vm.Graph(figure=fig_sbp),
        vm.Graph(figure=fig_sodium),
        
    ],
    controls=filters,
)

# Create the dashboard EXAMPLE USAGE
# dashboard = vm.Dashboard(pages=[page])


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

# Create the dashboard
dashboard = vm.Dashboard(pages=[page_0])

# Build and run the dashboard
Vizro().build(dashboard).run()
