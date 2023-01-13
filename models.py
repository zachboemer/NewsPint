from db import db


class Article(db.Model):
    __tablename__ = "articles"
    id = db.Column(db.Integer, primary_key=True)
    source_name = db.Column(db.String(255))
    title = db.Column(db.String(255))
    author = db.Column(db.String(255))
    publish_date = db.Column(db.DateTime)
    retrieval_date = db.Column(db.DateTime)
    url = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    summary = db.Column(db.String(255))

    def to_dict(self):
        return {
            'id': self.id,
            'source_name': self.source_name,
            'title': self.title,
            'author': self.author,
            'publish_date': self.publish_date,
            'retrieval_date': self.retrieval_date,
            'url': self.url,
            'image_url': self.image_url,
            'summary': self.summary
        }
