import pyodbc

dat = pyodbc.connect(driver    ="{iSeries Access ODBC Driver}",
                     database  ="S06F390T",
                     system    ="10.1.1.1",
                     uid       ="AUTOSQL",
                     pwd       ="AUTOSQL")

print(dat)

