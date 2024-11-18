from sqlalchemy import MetaData, Column, Integer, String, DateTime, func, CheckConstraint, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_`%(constraint_name)s`",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)

Base = declarative_base(metadata=metadata)

class Owner(Base):
    __tablename__ = "owners"

    __table_args__ = (
        CheckConstraint("length(name) > 0", name="ck_owners_name_length"),
        CheckConstraint("length(email) > 6", name="ck_owners_email_length"),
    )

    # column setup: type, any constraints?
    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False)
    email = Column(String(45), nullable=False, unique=True)
    phone = Column(String(25), nullable=False, unique=True)
    address = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    pets = relationship("Pet", back_populates="owner")

    def __repr__(self):
        return f"""
            Pet #{self.id}: {self.name}, {self.email}
        """

class Pet(Base):
    __tablename__ = "pets"

    __table_args__ = (
        CheckConstraint("length(name) > 0", name="ck_pets_name_length"),
    )

    # column setup: type, any constraints?
    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False)
    species = Column(String, nullable=False)
    breed = Column(String, nullable=False)
    temperament = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("owners.id")) #tablename.columnname
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    owner = relationship("Owner", back_populates="pets")

    def __repr__(self):
        return f"""
            Owner: #{self.id}, 
            Name: {self.name}, 
            Species: {self.species}, 
            Breed: {self.breed}
        """
