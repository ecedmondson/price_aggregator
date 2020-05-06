"""Writing to RST file until we have a better solution."""
import os
HEADERS = ["Product Name", "Price", "Photo", "Timestamp", "TTL"]


class RSTWriter:
    # This code has been borrowed
    # almost verbatim from this SO post:
    # https://stackoverflow.com/a/17203834
    # I will not be upset at all if, upon review,
    # the group decides to do something different
    # than RST writing (DB maybe?). However, the DB
    # isn't setup yet and I don't want us to get
    # banned from any websites for being robots.
    # Hence, this is solution for now.
    def table_div(self, max_cols, header_flag=1):
        out = ""
        if header_flag == 1:
            style = "="
        else:
            style = "-"

        for max_col in max_cols:
            out += max_col * style + " "

        out += "\n"
        return out

    def normalize_row(self, row, max_cols):
        r = ""
        for i, max_col in enumerate(max_cols):
            r += row[i] + (max_col - len(row[i]) + 1) * " "

        return r + "\n"

    def make_table(self, grid):
        max_cols = [
            max(out)
            for out in map(list, zip(*[[len(item) for item in row] for row in grid]))
        ]
        rst = self.table_div(max_cols, 1)

        for i, row in enumerate(grid):
            header_flag = False
            if i == 0 or i == len(grid) - 1:
                header_flag = True
            rst += self.normalize_row(row, max_cols)
            rst += self.table_div(max_cols, header_flag)
        return rst

    def normalize_filepath(self):
        if not os.path.exists('assets/data'):
            os.mkdir('assets/data')

    def write_table_to_file(self, filepath, grid, tablename="Product"):
        table = self.make_table(grid)
        self.normalize_filepath()
        print(filepath)
        file = open(filepath, "w+")
        header_format = "-" * (len(tablename) + 1)
        file.write(f"{tablename}\n")
        file.write(f"{header_format}\n")
        file.write(table)
        file.close()
