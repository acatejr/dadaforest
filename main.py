from sqlalchemy.orm import Session
from sqlalchemy import or_, select
from crawlers.crawlers import data_dot_gov, fsgeodata, climate_risk_viewer
from metadata_urls import data_dot_gov_urls, fsgeodata_urls, crv_urls
from models import Asset, Domains, Keyword, AssetKeyword
import database


def show_all_assets():
    with Session(autoflush=True, bind=database.engine) as session:
        import icecream

        assets = session.query(Asset).all()
        for asset in assets:
            icecream.ic(asset)
            for kw in asset.keywords:
                icecream.ic(kw.keyword)


def main():
    assets = data_dot_gov(data_dot_gov_urls)
    assets.extend(fsgeodata(fsgeodata_urls))
    assets.extend(climate_risk_viewer(crv_urls))

    for a in assets:
        keywords = []
        with Session(autoflush=True, bind=database.engine) as session:
            keywords = []
            for kw in a["keywords"]:
                keywords.append(Keyword(word=kw))
            session.add_all(keywords)
            session.commit()

            asset = session.execute(
                select(Asset).filter(
                    or_(
                        Asset.metadata_url == a["metadata_url"],
                        Asset.title == a["title"],
                    )
                )
            ).scalar_one_or_none()

            if asset:
                asset.title = a["title"]
                asset.description = a["description"]
                asset.metadata_url = a["metadata_url"]
                asset.domain = Domains.DATA_DOT_GOV
            else:
                asset = Asset(
                    title=a["title"],
                    description=a["description"],
                    metadata_url=a["metadata_url"],
                    domain=Domains.DATA_DOT_GOV,
                )

            for kw in keywords:
                asset.keywords.append(AssetKeyword(kw))

            session.add(asset)
            session.commit()

    show_all_assets()


if __name__ == "__main__":
    main()
