
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
