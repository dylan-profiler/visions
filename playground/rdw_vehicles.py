import pandas as pd
import numpy as np

from tenzing.core.model import tenzing_complete_set, type_cast, type_inference
from tenzing.core.summaries.summary import summary


# file_name = "https://opendata.rdw.nl/api/views/m9d7-ebf2/rows.csv?accessType=DOWNLOAD"
file_name = r"C:\Users\Cees Closed\Downloads\Open_Data_RDW__Gekentekende_voertuigen.csv"

# Load dataset
df = pd.read_csv(
    file_name,
    dtype={
        'WAM verzekerd': 'category',
        'Wacht op keuren': 'category',
        'Eerste kleur': 'category',
        'Tweede kleur': 'category',
        'Merk': 'category',
        'Zuinigheidslabel': 'category',
        'Inrichting': 'category',
        'Voertuigsoort': 'category',
        'Retrofit roetfilter': 'category',
        # 'Bruto BPM': 'Int32',
        # 'Aantal zitplaatsen': 'Int8',
        # 'Aantal cilinders': 'Int16',

    },
    parse_dates=[
      "Vervaldatum tachograaf"
    ],
    nrows=100000,
    low_memory=True
)


start = df.memory_usage(deep=True).sum()

# df['Pclass'] = pd.Categorical(df['Pclass'], categories=sorted(df['Pclass'].unique()), ordered=True)
# df['Vervaldatum tachograaf'] = pd.to_datetime(df['Vervaldatum tachograaf'])
df['Bruto BPM'] = df['Bruto BPM'].astype('Int32')
df['Aantal cilinders'] = df['Aantal cilinders'].astype('Int16')
df['Aantal zitplaatsen'] = df['Aantal zitplaatsen'].astype("Int8")
# df['Eerste kleur'] = df['Eerste kleur'].astype('category')
# df['Tweede kleur'] = df['Tweede kleur'].astype('category')
# df['Voertuigsoort'] = df['Voertuigsoort'].astype('category')
# df['Merk'] = df['Merk'].astype('category')
# df['Inrichting'] = df['Inrichting'].astype('category')
# df['Zuinigheidslabel'] = df['Zuinigheidslabel'].astype('category')
# df['Wacht op keuren'] = df['Wacht op keuren'].astype('category')
# df['WAM verzekerd'] = df['WAM verzekerd'].astype('category')
# df['Retrofit roetfilter'] = df['Retrofit roetfilter'].astype('category')

end = df.memory_usage(deep=True).sum()

print(f"Initial {start} bytes reduced to {end} bytes. Difference {start - end} bytes. Reduction of {(start-end) / start:.0%}")

exit()
# Type
typeset = tenzing_complete_set()

# Type inference
inferred_types = type_inference(df, typeset)
print(inferred_types)

# Type cast
cast_df, cast_types = type_cast(df, typeset)
print(cast_types)

# Summarization
summaries = summary.summarize(cast_df, cast_types)
for key, variable_summary in summaries["series"].items():
    print(key, variable_summary)
