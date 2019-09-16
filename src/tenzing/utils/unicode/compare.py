import unicodedata
from tenzing.utils.unicode import unicode_data


if __name__ == "__main__":
    for char in ["Ф", "A", "$", " ", "\n", "/", "9", "a", "\u0660"]:
        # Corresponding operations to unicodedata
        print("-----------------------------------------------")
        print(repr(char))
        try:
            print("Name", unicode_data.name(char), unicodedata.name(char))
        except ValueError:
            pass
        try:
            print("Decimal", unicode_data.decimal(char), unicodedata.decimal(char))
            print("Digit", unicode_data.digit(char), unicodedata.digit(char))
            print("Numeric", unicode_data.numeric(char), unicodedata.numeric(char))
        except ValueError:
            pass
        print("Category", unicode_data.category(char), unicodedata.category(char))
        print(
            "Bidirectional",
            unicode_data.bidirectional(char),
            unicodedata.bidirectional(char),
        )
        print("Combining", unicode_data.combining(char), unicodedata.combining(char))
        print("Mirrored", unicode_data.mirrored(char), unicodedata.mirrored(char))
        print(
            "East Asian Width",
            unicode_data.east_asian_width(char),
            unicodedata.east_asian_width(char),
        )
        print(
            "Decomposition",
            unicode_data.decomposition(char),
            unicodedata.decomposition(char),
        )

        # Extended methods
        print("-----------------------------------------------")
        print("Category Alias", unicode_data.category_alias(char))
        print("East Asian Width Alias", unicode_data.east_asian_width_alias(char))
        print("Bidirectional Alias", unicode_data.bidirectional_alias(char))
        print("Script", unicode_data.script(char))
        print("Block", unicode_data.block(char))
        try:
            print("Proplist", unicode_data.proplist(char))
        except:
            pass
        print("-----------------------------------------------")
        print("")
