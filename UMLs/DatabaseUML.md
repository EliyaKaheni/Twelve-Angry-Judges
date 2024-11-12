Table users {
  id integer [unique]
  username varchar
  password varchar
}

Table courtCaseRecord {
  id integer [unique]
  username varchar
  conversation JSON
  created_at timestamp
}

Ref: users.username > courtCaseRecord.username
