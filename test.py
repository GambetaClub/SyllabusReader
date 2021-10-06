import os
import sys
import pandas as pd
from docx import Document

def read_docx_table(document, table_num=1,nheader=1):
    table = document.tables[table_num-1]
    data = [[cell.text for cell in row.cells] for row in table.rows]
    df = pd.DataFrame(data)
    if nheader == 1:
        df = df.rename(columns=df.iloc [0]).drop (df.index [0]).reset_index(drop=True)
    elif nheader == 2:
        outside_col, inside_col = df.iloc[0], df.iloc [1]
        hier_index = pd.MultiIndex.from_tuples (list (zip(outside_col, inside_col)))
        df = pd.DataFrame(data, columns=hier_index).drop(df.index[[0,1]]).reset_index(drop=True)
    elif nheader > 2:
        print("More than two headers not currently supported")
        df = pd.DataFrame()
    return df

def main():

    if len(sys.argv) != 2:
        sys.exit("Usage: python3 test.py <directory_name>")

    document = Document(os.path.join(sys.argv[1], 'Syllabus1.docx'))
    df = read_docx_table(document, 1, 2)
    print(df)


if __name__ == "__main__":
    main()