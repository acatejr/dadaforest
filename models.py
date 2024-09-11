from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String, Text, Enum
from sqlalchemy.orm import relationship, DeclarativeBase
import enum


class Domains(enum.Enum):
    EDW = 1
    DATA_DOT_GOV = 2
    FS_GEODATA = 3
    CRV = 4


class Visibility(enum.Enum):
    PUBLIC = 1
    INTERNAL = 2


class Base(DeclarativeBase):
    pass


class Asset(Base):
    __tablename__ = "asset"

    id = Column(Integer, primary_key=True)
    title = Column(String(300), nullable=True, unique=True)
    description = Column(Text, nullable=True, unique=False)
    metadata_url = Column(String(500), nullable=True, unique=True)
    visibility = Column(
        Enum(Visibility), nullable=False, unique=False, default=Visibility.PUBLIC
    )
    domain = Column(Enum(Domains), nullable=False, default=Domains.EDW)
    keywords = relationship(
        "AssetKeyword", cascade="all, delete-orphan", backref="asset"
    )

    def __init__(self, title, description=None, metadata_url=None, domain=Domains.EDW):
        self.domain = domain
        self.title = title
        if description:
            self.description = description
        if metadata_url:
            self.metadata_url = metadata_url

    def __str__(self):
        return f"{self.title}"

    def __repr__(self):
        return f"Asset({self.title})"


class Keyword(Base):
    __tablename__ = "keyword"

    id = Column(Integer, primary_key=True)
    word = Column(String(300), nullable=False, unique=False)

    def __init__(self, word):
        self.word = word

    def __str__(self):
        return f"{self.word}"

    def __repr__(self):
        return f"Asset({self.word})"


class AssetKeyword(Base):
    __tablename__ = "assetkeyword"

    asset_id = Column(Integer, ForeignKey("asset.id"), primary_key=True)
    keyword_id = Column(Integer, ForeignKey("keyword.id"), primary_key=True)

    def __init__(self, keyword, word=None):
        self.keyword = keyword
        self.word = word

    keyword = relationship(Keyword, lazy="joined")
