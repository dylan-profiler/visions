from tenzing.summary import summary_report


class tenzing_typeset:
    def __init__(self, types):
        self.types = frozenset(types)

        self.relation_map = {typ: {} for typ in self.types}
        for typ in self.types:
            for friend_type, relation in typ.relations.items():
                self.relation_map[friend_type][typ] = relation


class tenzingTypeset(tenzing_typeset):
    def __init__(self, types):
        self.column_summary = {}
        super().__init__(types)

    def prep(self, df):
        self.column_type_map = {col: self._get_column_type(df[col]) for col in df.columns}
        self.is_prepped = True
        return self

    def summarize(self, df):
        assert self.is_prepped, "typeset hasn't been prepped for your dataset yet. Call .prep(df)"
        summary = {col: self.column_type_map[col].summarize(df[col]) for col in df.columns}
        self.column_summary = summary
        return self.column_summary

    def general_summary(self, df):
        summary = {}
        summary['Number of Observations'] = df.shape[0]
        summary['Number of Variables'] = df.shape[1]
        return summary

    def summary_report(self, df):
        general_summary = self.general_summary(df)
        column_summary = self.summarize(df)
        return summary_report(self.column_type_map, column_summary, general_summary)

    def _get_column_type(self, series):
        # walk the relation_map to determine which is most uniquely specified
        candidates = [tenzing_type for tenzing_type in self.types if series in tenzing_type]
        if len(candidates) > 1:
            print("You forgot to implement handling for multiple matches. Go fix that retard")
        return candidates[0]
