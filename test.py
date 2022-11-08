from src.helper.model.table import (
    NullForeignKey,
    PrimaryKey,
    PrimaryWithForeignKey,
)

n_key = NullForeignKey(
    from_table="Artist", to="AlbumID", name="AlbumID", type="int"
)
p_k = PrimaryKey(name="Name", type="int")
pf = PrimaryWithForeignKey(
    name="AlbumID", type="int", from_table="Artist", to="AlbumID"
)

print(n_key)
print(p_k)
print(pf)
