from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import enum
from sqlalchemy import Enum, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from .extensions import db
from datetime import datetime
from flask_login import UserMixin


class UserRoleEnum(enum.Enum):
    Admin = "Admin"
    Regular = "Regular"


class TransactionStatus(enum.Enum):
    Pending = "Pending"
    Accepted = "Accepted"
    Completed = "Completed"
    Cancelled = "Cancelled"


class GenreType(enum.Enum):
    Novel = "Novel"
    Adventure = "Adventure"
    Fiction = "Fiction"
    Science = "Science"
    CrimeHorror = "Crime/Horror"
    Poetry = "Poetry"


class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    UserID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String)
    Email = db.Column(db.String)
    PasswordHash = db.Column(db.String)
    UserRole = db.Column(Enum(UserRoleEnum))
    RegistrationDate = db.Column(db.DateTime)
    DeletedAt = db.Column(db.DateTime)

    def get_id(self):
        return str(self.UserID)


class Inventory(db.Model):
    __tablename__ = 'inventory'
    BookID = db.Column(db.Integer, primary_key=True)
    OwnerID = db.Column(db.Integer, db.ForeignKey('users.UserID'))
    Title = db.Column(db.String)
    Author = db.Column(db.String)
    Genre = db.Column(Enum(GenreType))
    Status = db.Column(db.Boolean, default=False)
    DeletedAt = db.Column(db.DateTime)
    CreatedAt = db.Column(db.DateTime)


class Prompts(db.Model):
    __tablename__ = 'prompts'
    PromptID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('users.UserID'))
    SubmissionDate = db.Column(db.DateTime, default=datetime.utcnow)
    Name = db.Column(db.Text)
    messages = db.relationship('PromptMessages', backref='prompt', lazy=True)


class PromptMessages(db.Model):
    __tablename__ = 'prompt_messages'
    MessageID = db.Column(db.Integer, primary_key=True)
    PromptID = db.Column(db.Integer, db.ForeignKey('prompts.PromptID'))
    MessageText = db.Column(db.Text, nullable=False)
    IsResponse = db.Column(db.Boolean, default=False)
    Timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Chats(db.Model):
    __tablename__ = 'chats'
    ChatID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('users.UserID'))
    StartDate = db.Column(db.DateTime)
    EndDate = db.Column(db.DateTime)


class ChatMessages(db.Model):
    __tablename__ = 'chat_messages'
    MessageID = db.Column(db.Integer, primary_key=True)
    ChatID = db.Column(db.Integer, db.ForeignKey('chats.ChatID'))
    UserID = db.Column(db.Integer, db.ForeignKey('users.UserID'))
    MessageText = db.Column(db.Text)
    Timestamp = db.Column(db.DateTime)


class Transactions(db.Model):
    __tablename__ = 'transactions'
    TransactionID = db.Column(db.Integer, primary_key=True)
    ReceiverBookID = db.Column(db.Integer, db.ForeignKey('inventory.BookID'))
    SenderBookID = db.Column(db.Integer, db.ForeignKey('inventory.BookID'))
    ReceiverID = db.Column(db.Integer, db.ForeignKey('users.UserID'))
    SenderID = db.Column(db.Integer, db.ForeignKey('users.UserID'))
    TransactionDate = db.Column(db.DateTime)
    Status = db.Column(Enum(TransactionStatus))


class Reviews(db.Model):
    __tablename__ = 'reviews'
    ReviewID = db.Column(db.Integer, primary_key=True)
    BookID = db.Column(db.Integer, db.ForeignKey('inventory.BookID'))
    UserID = db.Column(db.Integer, db.ForeignKey('users.UserID'))
    Rating = db.Column(db.Integer)
    ReviewText = db.Column(db.Text)
    ReviewDate = db.Column(db.DateTime)


class UploadedFiles(db.Model):
    __tablename__ = 'uploaded_files'
    FileID = db.Column(db.Integer, primary_key=True)
    PromptID = db.Column(db.Integer, db.ForeignKey('prompts.PromptID'), nullable=False)
    UserID = db.Column(db.Integer, db.ForeignKey('users.UserID'), nullable=False)
    FileName = db.Column(db.String(256), nullable=False)
    FilePath = db.Column(db.String(512), nullable=False)
    UploadDate = db.Column(db.DateTime, default=datetime.utcnow)
