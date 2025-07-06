-- Create the user if it doesn't exist
DO
$$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles WHERE rolname = 'devtedsuser'
   ) THEN
      CREATE ROLE devtedsuser WITH LOGIN PASSWORD 'devtedspass';
   END IF;
END
$$;

-- Grant privileges to the user
GRANT ALL PRIVILEGES ON DATABASE quotevault TO devtedsuser;

-- Connect to the database
\c quotevault;

-- Create the quotes table
CREATE TABLE IF NOT EXISTS quotes (
    id SERIAL PRIMARY KEY,
    quote TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Grant table privileges to the user
GRANT ALL PRIVILEGES ON TABLE quotes TO devtedsuser;
GRANT ALL PRIVILEGES ON SEQUENCE quotes_id_seq TO devtedsuser;

-- Insert some sample data
INSERT INTO quotes (quote) VALUES 
('The only way to do great work is to love what you do. - Steve Jobs'),
('Innovation distinguishes between a leader and a follower. - Steve Jobs'),
('Life is what happens to you while you''re busy making other plans. - John Lennon')
ON CONFLICT DO NOTHING;