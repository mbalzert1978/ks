from __future__ import annotations
from datetime import date
from decimal import Decimal
from sqlmodel import Field, SQLModel
import ipaddress


class Address(SQLModel):
    address: str = Field(alias="Address")
    city: str = Field(alias="City")
    state: str = Field(alias="State")
    country: str = Field(alias="Country")
    postal_code: str = Field(alias="PostalCode")
    phone: str | None = Field(alias="Phone")
    fax: str | None = Field(alias="Fax")


class Album(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, alias="AlbumId")
    title: str = Field(alias="Title")
    artist_id: int = Field(alias="ArtistId", foreign_key="Artist.id")


class Artist(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, alias="ArtistId")
    name: str = Field(alias="Name")


class Customer(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, alias="CustomerId")
    first_name: str = Field(alias="Name")
    last_name: str = Field(alias="Name")
    company: str | None = Field(alias="Name")
    address: Address | None
    email: str = Field(alias="Name")
    support_rep_id: str | None = Field(
        alias="SupportRepId", foreign_key="Employee.id"
    )


class Employee(SQLModel, table=True):
    id: str | None = Field(alias="EmployeeId")
    last_name: str = Field(alias="LastName")
    first_name: str = Field(alias="FirstName")
    title: str = Field(alias="Title")
    birth_date: date = Field(alias="BirthDate")
    hire_date: date = Field(alias="HireDate")
    address: Address | None
    email: str = Field(alias="Email")
    reports_to: str = Field(alias="ReportsTo", foreign_key="Employee.id")


class Genre(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, alias="GenreID")
    name: str = Field(alias="Name")


class Invoice(SQLModel, table=True):
    id: int | None = Field(alias="InvoiceId", primary_key=True)
    invoice_date: date = Field(alias="InvoiceDate")
    billing_address: Address | None = Field(alias="BillingAddress")
    total: str = Field(alias="Total")
    customer_id: str = Field(alias="CustomerId", foreign_key="Customer.id")


class InvoiceLine(SQLModel, table=True):
    id: int | None = Field(alias="InvoiceLineId", primary_key=True)
    invoice_id: int = Field(alias="InvoiceId", foreign_key="Invoice.id")
    track_id: int = Field(alias="TrackId", foreign_key="Track.id")
    unit_price: Decimal = Field(alias="UnitPrice")
    Quantity: int = Field(alias="Quantity")


class MediaType(SQLModel, table=True):
    id: int | None = Field(alias="MediaTypeId", primary_key=True)
    name: str = Field(alias="Name")


class Playlist(SQLModel, table=True):
    id: int | None = Field(alias="PlaylistId", primary_key=True)
    name: str = Field(alias="Name")


class PlaylistTrack(SQLModel, table=True):
    playlist_id: int | None = Field(
        alias="PlaylistId",
        primary_key=True,
        foreign_key="Playlist.id",
    )
    track_id: int | None = Field(
        alias="TrackId",
        primary_key=True,
        foreign_key="Track.id",
    )


class Track(SQLModel, table=True):
    id: int | None = Field(alias="TrackId", primary_key=True)
    name: str = Field(alias="Name")
    album_id: int = Field(alias="AlbumId", foreign_key="Album.id")
    media_type_id: int = Field(alias="MediaTypeId", foreign_key="MediaType.id")
    genre_id: int = Field(alias="GenreId", foreign_key="Genre.id")
    composer: str = Field(alias="Composer")
    milliseconds: int = Field(alias="Milliseconds")
    bytes: int = Field(alias="Bytes")
    unit_price: Decimal = Field(alias="UnitPrice")
