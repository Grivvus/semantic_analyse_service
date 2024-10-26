import pathlib

import pandas
import weaviate
import weaviate.classes as wvc

from app.logic import connect_to_vec_db
from app.model import vectorize_one

path = str(pathlib.Path(__file__).parent.parent) + "/data/"


def declare_schemas():
    client = connect_to_vec_db()
    try:
        issues = client.collections.create(
            name="Issue",
            vectorizer_config=wvc.config.Configure.Vectorizer.none(),
            properties=[
                wvc.config.Property(
                    name="issue_id",
                    data_type=wvc.config.DataType.INT,
                ),
                wvc.config.Property(
                    name="issue_text",
                    data_type=wvc.config.DataType.TEXT,
                ),
                wvc.config.Property(
                    name="label",
                    data_type=wvc.config.DataType.TEXT,
                ),
                wvc.config.Property(
                    name="solution",
                    data_type=wvc.config.DataType.TEXT,
                )
            ],
        )
        print(issues.config.get(simple=False))
    finally:
        client.close()


def fillup_db():
    client = connect_to_vec_db()
    try:
        collection = client.collections.get("Issue")
        data = prepare_data()
        collection.data.insert_many(data)
    finally:
        client.close()


def prepare_data() -> list[wvc.data.DataObject]:
    print(path)
    df = pandas.read_csv(path + "out.csv", dialect="excel")
    res = []
    for i, row in df.iterrows():
        vector = vectorize_one(row["Topic"])
        res.append(
            wvc.data.DataObject(
                properties={
                    "issue_id": row["№"],
                    "issue_text": row["Topic"],
                    "label": row["label"],
                    "Solution": row["Solution"],
                },
                vector=vector
            )
        )
    return res
