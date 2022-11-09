from __future__ import annotations
from datetime import date
from sqlmodel import SQLModel
from sqlmodel import Field


class Album(SQLModel, table=True):
    AlbumId: int | None = Field(default=None, primary_key=True)
    Title: str
    ArtistId: int = Field(foreign_key='Artist.ArtistId')


class Artist(SQLModel, table=True):
    ArtistId: int | None = Field(default=None, primary_key=True)
    Name: str | None = Field(default=None)


class Customer(SQLModel, table=True):
    CustomerId: int | None = Field(default=None, primary_key=True)
    FirstName: str
    LastName: str
    Company: str | None = Field(default=None)
    Address: str | None = Field(default=None)
    City: str | None = Field(default=None)
    State: str | None = Field(default=None)
    Country: str | None = Field(default=None)
    PostalCode: str | None = Field(default=None)
    Phone: str | None = Field(default=None)
    Fax: str | None = Field(default=None)
    Email: str
    SupportRepId: int | None = Field(
        default=None, foreign_key='Employee.EmployeeId'
    )


class Employee(SQLModel, table=True):
    EmployeeId: int | None = Field(default=None, primary_key=True)
    LastName: str
    FirstName: str
    Title: str | None = Field(default=None)
    ReportsTo: int | None = Field(
        default=None, foreign_key='Employee.EmployeeId'
    )
    BirthDate: date | None = Field(default=None)
    HireDate: date | None = Field(default=None)
    Address: str | None = Field(default=None)
    City: str | None = Field(default=None)
    State: str | None = Field(default=None)
    Country: str | None = Field(default=None)
    PostalCode: str | None = Field(default=None)
    Phone: str | None = Field(default=None)
    Fax: str | None = Field(default=None)
    Email: str | None = Field(default=None)


class Genre(SQLModel, table=True):
    GenreId: int | None = Field(default=None, primary_key=True)
    Name: str | None = Field(default=None)


class Invoice(SQLModel, table=True):
    InvoiceId: int | None = Field(default=None, primary_key=True)
    CustomerId: int = Field(foreign_key='Customer.CustomerId')
    InvoiceDate: date
    BillingAddress: str | None = Field(default=None)
    BillingCity: str | None = Field(default=None)
    BillingState: str | None = Field(default=None)
    BillingCountry: str | None = Field(default=None)
    BillingPostalCode: str | None = Field(default=None)
    Total: str


class InvoiceLine(SQLModel, table=True):
    InvoiceLineId: int | None = Field(default=None, primary_key=True)
    InvoiceId: int = Field(foreign_key='Invoice.InvoiceId')
    TrackId: int = Field(foreign_key='Track.TrackId')
    UnitPrice: str
    Quantity: int


class MediaType(SQLModel, table=True):
    MediaTypeId: int | None = Field(default=None, primary_key=True)
    Name: str | None = Field(default=None)


class Playlist(SQLModel, table=True):
    PlaylistId: int | None = Field(default=None, primary_key=True)
    Name: str | None = Field(default=None)


class PlaylistTrack(SQLModel, table=True):
    PlaylistId: int | None = Field(
        default=None, primary_key=True, foreign_key='Playlist.PlaylistId'
    )
    TrackId: int | None = Field(
        default=None, primary_key=True, foreign_key='Track.TrackId'
    )


class Track(SQLModel, table=True):
    TrackId: int | None = Field(default=None, primary_key=True)
    Name: str
    AlbumId: int | None = Field(default=None, foreign_key='Album.AlbumId')
    MediaTypeId: int = Field(foreign_key='MediaType.MediaTypeId')
    GenreId: int | None = Field(default=None, foreign_key='Genre.GenreId')
    Composer: str | None = Field(default=None)
    Milliseconds: int
    Bytes: int | None = Field(default=None)
    UnitPrice: str
