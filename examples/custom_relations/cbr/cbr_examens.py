import pandas as pd

df = pd.read_csv(
    "https://www.cbr.nl/web/file?uuid=22431038-3c85-4f23-8203-ce90afbecc94&owner=d214f7b5-5ce0-48dc-a521-4ef537c9d232&contentid=11702",
    sep=";",
)
print(df.head().to_string())
