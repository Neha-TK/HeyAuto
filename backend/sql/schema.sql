CREATE TABLE IF NOT EXISTS users (
  id serial PRIMARY KEY,
  name text NOT NULL,
  email text UNIQUE NOT NULL,
  password text NOT NULL,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS autostands (
  id serial PRIMARY KEY,
  name text NOT NULL,
  location text NOT NULL
);

CREATE TABLE IF NOT EXISTS drivers (
  id serial PRIMARY KEY,
  name text NOT NULL,
  phone text UNIQUE,
  password text NOT NULL,
  is_available boolean DEFAULT false,
  stand_id integer REFERENCES autostands(id),
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS rides (
  id serial PRIMARY KEY,
  user_id integer REFERENCES users(id),
  driver_id integer REFERENCES drivers(id),
  start_location text NOT NULL,
  end_location text NOT NULL,
  status text DEFAULT 'pending',
  requested_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS stand_queue (
  id serial PRIMARY KEY,
  stand_id integer NOT NULL REFERENCES autostands(id),
  driver_id integer NOT NULL REFERENCES drivers(id),
  joined_at timestamptz DEFAULT now(),
  status text DEFAULT 'waiting'
);
