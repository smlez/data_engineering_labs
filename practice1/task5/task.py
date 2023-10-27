import pandas

pandas.read_html(open('text_5_var_72', 'r').read())[0].to_csv('result.csv')