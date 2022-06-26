#! /bin/bash

# to insert into local postgres database
  # before beginning make sure to have the postgres PATH configured on your OS

# create initial variable to connect to postgres to create a database or login
PSQL="psql -U postgres -c"
NAME="mays_taste"
DB_USERNAME="baryon"
if (psql -lqt | cut -d \| -f 1 | grep -qw "$NAME")
then
  PSQL="psql --username=$DB_USERNAME --dbname=$NAME --tuples-only -c"
else
  CREATE_DATABASE=$($PSQL "CREATE DATABASE $NAME;")
  echo -e "\nDatabase $NAME was created."
  PSQL="psql --username=$DB_USERNAME --dbname=$NAME --tuples-only -c"

  # create table
  TABLE_NAME='videos'
  $PSQL "CREATE TABLE $TABLE_NAME(
  video_id VARCHAR(100) UNIQUE PRIMARY KEY,
  video_title VARCHAR(100) NOT NULL,
  upload_date DATE NOT NULL,
  view_count INT NOT NULL,
  like_count INT NOT NULL,
  comment_count INT NOT NULL);"

  echo -e "\nTable $TABLE_NAME created."
fi

# insert csv into database
FNAME="mays_taste_yt.csv"
cat $FNAME | while IFS="\$" read NUMBER VIDEO_ID VIDEO_TITLE UPLOAD_DATE VIEW_COUNT LIKE_COUNT COMMENT_COUNT
do
  # prevent name of columns to be added into the database
  if [[ $VIDEO_ID != 'video_id' ]]
  then
    # video_id if exists (update) if not insert
    GET_VIDEO_ID=$($PSQL "SELECT video_id FROM videos WHERE video_id='$VIDEO_ID';")
    if [[ -z $GET_VIDEO_ID ]]
    then
      INSERT_VIDEO_ID=$($PSQL "INSERT INTO videos (video_id, video_title, upload_date, view_count, like_count, comment_count)
      VALUES ('$VIDEO_ID', '$VIDEO_TITLE', '$UPLOAD_DATE', $VIEW_COUNT, $LIKE_COUNT, $COMMENT_COUNT);")
    # update video
    else
      UPDATE_VIDEO=$($PSQL "UPDATE videos SET
      video_title='$VIDEO_TITLE',
      upload_date='$UPLOAD_DATE',
      view_count=$VIEW_COUNT,
      like_count=$LIKE_COUNT,
      comment_count=$COMMENT_COUNT
      WHERE video_id='$VIDEO_ID';")

    fi
  fi
done
