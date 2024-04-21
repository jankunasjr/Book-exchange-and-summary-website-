CREATE TYPE UserRoleEnum AS ENUM ('Admin', 'Premium', 'Regular');

-- Users Table
CREATE TABLE "users" (
    "UserID" SERIAL PRIMARY KEY,
    "Username" VARCHAR,
    "Email" VARCHAR,
    "PasswordHash" VARCHAR,
    "UserRole" UserRoleEnum,
    "RegistrationDate" TIMESTAMP,
    "DeletedAt" TIMESTAMP
);

-- Inventory Table
CREATE TABLE "inventory" (
    "BookID" SERIAL PRIMARY KEY,
    "OwnerID" INTEGER REFERENCES "users"("UserID"),
    "Title" VARCHAR,
    "Author" VARCHAR,
    "Genre" VARCHAR,
    "Status" BOOLEAN DEFAULT false,
    "DeletedAt" TIMESTAMP,
    "CreatedAt" TIMESTAMP
);

-- Prompts Table
CREATE TABLE "prompts" (
    "PromptID" SERIAL PRIMARY KEY,
    "UserID" INTEGER REFERENCES "users"("UserID"),
    "SubmissionDate" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "Name" TEXT
);

-- Prompt Messages Table
CREATE TABLE "prompt_messages" (
    "MessageID" SERIAL PRIMARY KEY,
    "PromptID" INTEGER REFERENCES "prompts"("PromptID"),
    "MessageText" TEXT NOT NULL,
    "IsResponse" BOOLEAN DEFAULT false,
    "Timestamp" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Chats Table
CREATE TABLE "chats" (
    "ChatID" SERIAL PRIMARY KEY,
    "UserID" INTEGER REFERENCES "users"("UserID"),
    "StartDate" TIMESTAMP,
    "EndDate" TIMESTAMP
);

-- Chat Messages Table
CREATE TABLE "chat_messages" (
    "MessageID" SERIAL PRIMARY KEY,
    "ChatID" INTEGER REFERENCES "chats"("ChatID"),
    "UserID" INTEGER REFERENCES "users"("UserID"),
    "MessageText" TEXT,
    "Timestamp" TIMESTAMP
);

-- Transactions Table
CREATE TABLE "transactions" (
    "TransactionID" SERIAL PRIMARY KEY,
    "ReceiverBookID" INTEGER REFERENCES "inventory"("BookID"),
    "SenderBookID" INTEGER REFERENCES "inventory"("BookID"),
    "ReceiverID" INTEGER REFERENCES "users"("UserID"),
    "SenderID" INTEGER REFERENCES "users"("UserID"),
    "TransactionDate" TIMESTAMP,
    "Status" VARCHAR
);

-- Reviews Table
CREATE TABLE "reviews" (
    "ReviewID" SERIAL PRIMARY KEY,
    "BookID" INTEGER REFERENCES "inventory"("BookID"),
    "UserID" INTEGER REFERENCES "users"("UserID"),
    "Rating" INTEGER,
    "ReviewText" TEXT,
    "ReviewDate" TIMESTAMP
);

-- Uploaded Files Table
CREATE TABLE "uploaded_files" (
    "FileID" SERIAL PRIMARY KEY,
    "PromptID" INTEGER REFERENCES "prompts"("PromptID") NOT NULL,
    "UserID" INTEGER REFERENCES "users"("UserID") NOT NULL,
    "FileName" VARCHAR(256) NOT NULL,
    "FilePath" VARCHAR(512) NOT NULL,
    "UploadDate" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Insert users
INSERT INTO users ("Username", "Email", "PasswordHash", "UserRole", "RegistrationDate") VALUES
('JohnDoe', 'admin@admin.com', 'admin', 'Admin', '2023-04-15'),
('JaneSmith', 'jane@example.com', 'hashed_password', 'Premium', '2023-04-15'),
('AliceJohnson', 'alice@example.com', 'hashed_password', 'Regular', '2023-04-15');

-- Insert inventory items
INSERT INTO inventory ("OwnerID", "Title", "Author", "Genre", "Status", "CreatedAt") VALUES
(1, 'The Great Gatsby', 'F. Scott Fitzgerald', 'Fiction', FALSE, '2023-04-15'),
(2, '1984', 'George Orwell', 'Dystopian', TRUE, '2023-04-15'),
(1, 'To Kill a Mockingbird', 'Harper Lee', 'Fiction', FALSE, '2023-04-15');

-- Insert prompts
INSERT INTO prompts ("UserID", "SubmissionDate", "Name") VALUES
(1, '2023-04-15', 'Test prompt'),
(2, '2023-04-15', 'Writing Tips'),
(3, '2023-04-15', 'Book Review Guidelines');

-- Insert prompt messages
INSERT INTO prompt_messages ("PromptID", "MessageText", "IsResponse", "Timestamp") VALUES
(1, 'How can I improve my writing?', FALSE, '2023-04-15'),
(1, 'Try focusing on your narrative structure.', TRUE, '2023-04-15');

-- Insert chats
INSERT INTO chats ("UserID", "StartDate", "EndDate") VALUES
(1, '2023-04-15', '2023-04-15'),
(2, '2023-04-15', '2023-04-15');

-- Insert chat messages
INSERT INTO chat_messages ("ChatID", "UserID", "MessageText", "Timestamp") VALUES
(1, 1, 'Hello, how can I help you today?', '2023-04-15'),
(1, 2, 'I need help with my account.', '2023-04-15');

-- Insert transactions
INSERT INTO transactions ("ReceiverBookID", "SenderBookID", "ReceiverID", "SenderID", "TransactionDate", "Status") VALUES
(2, 3, 2, 1, '2023-04-15', 'Completed');

-- Insert reviews
INSERT INTO reviews ("BookID", "UserID", "Rating", "ReviewText", "ReviewDate") VALUES
(3, 2, 5, 'An excellent read with profound characters.', '2023-04-15');

-- Insert uploaded files
INSERT INTO uploaded_files ("PromptID", "UserID", "FileName", "FilePath", "UploadDate") VALUES
(1, 2, 'writing_tips.pdf', '/files/writing_tips.pdf', '2023-04-15');
