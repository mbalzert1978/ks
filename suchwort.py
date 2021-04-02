import sqlite3, argparse #import der lib
from openpyxl import Workbook #import der lib

parser = argparse.ArgumentParser()
parser.add_argument('--search', action='store',
                    dest='search_',
                    help='Store a table', default="Rock")
searching_ = parser.parse_args()

conn = sqlite3.connect("Chinook_Sqlite_AutoIncrementPKs.sqlite")
cur = conn.cursor()
# Ansprechen der lokalen sqlite Datenbank
cur.execute(f"select name as Songtitel,                                                 \
                (select Artist.Name from Artist                                         \
                    WHERE Track.GenreId = Artist.ArtistId) AS Kuenstler,                \
                (select MediaType.Name from MediaType                                   \
                    WHERE Track.GenreId = MediaType.MediaTypeId) AS Mediatypname,		\
                (select Genre.Name from Genre                                           \
                    WHERE Track.GenreId = Genre.GenreId) AS Genrename,                  \
                (select Album.Title from Album                                          \
                    WHERE Track.GenreId = Album.AlbumId) AS Albumname                   \
                from Track                                                              \
                where name like '%{searching_.search_}%'                                \
                order by AlbumId                                                        \
                        ;")


list_data = cur.fetchall()
dict_ = {}
for item in list_data:
    a, b, c, d, e = item
    if e in dict_:
        dict_[e] += (a, b, c, d)
    else:
        dict_.update({e : (a,b,c,d)})
        
wb = Workbook()
ws = wb.worksheets[0]
ccount = 1
rcount = 2
sheetcount = 1
for key, value in dict_.items():
    if len(key) > 15:
        key = key[0:14] + "..."
    if ws.title == "Sheet":
        ws.title = key
        _ = ws.cell(column=1, row=1, value="Songtitel")
        _ = ws.cell(column=2, row=1, value="Künstler")
        _ = ws.cell(column=3, row=1, value="Mediatyp")
        _ = ws.cell(column=4, row=1, value="Genre")
        for item in value:
            if ccount  <=4:
                _ = ws.cell(column=ccount, row=rcount, value=item)
                ccount +=1
            else:
                ccount = 1
                _ = ws.cell(column=ccount, row=rcount+1, value=item)
                ccount = 2
                rcount +=1
        rcount = 1
    else:
        wb.create_sheet(key)
        ws = wb.worksheets[sheetcount]
        _ = ws.cell(column=1, row=1, value="Songtitel")
        _ = ws.cell(column=2, row=1, value="Künstler")
        _ = ws.cell(column=3, row=1, value="Mediatyp")
        _ = ws.cell(column=4, row=1, value="Genre")
        for item in value:
            if ccount  <=4:
                _ = ws.cell(column=ccount, row=rcount, value=item)
                ccount +=1
            else:
                ccount = 1
                _ = ws.cell(column=ccount, row=rcount+1, value=item)
                ccount = 2
                rcount +=1 
        sheetcount += 1
        rcount = 1
wb.save(f"{searching_.search_}.xlsx")

conn.close() 
