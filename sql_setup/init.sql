create database archive_no_stopwords;
use archive_no_stopwords;

create table threads(
    id INT NOT NULL PRIMARY KEY,
    post_date TIMESTAMP,
    unique_ips TINYINT UNSIGNED NOT NULL
);

create table words(
    thread_id INT,
    FOREIGN KEY (thread_id) REFERENCES threads(id),
    word VARCHAR(100) NOT NULL,
    occurences SMALLINT UNSIGNED NOT NULL
);

DELETE FROM threads;

INSERT INTO threads
VALUES (2, FROM_UNIXTIME(104112990), 104112990, 12, 12, 12);

INSERT INTO words (thread_id, word, occurences)
VALUES(5, "heloo", 1)

-- Get top 200 words in a time range
SELECT word, SUM(occurences) as total_occurences 
FROM words 
WHERE words.thread_id IN 
(SELECT threads.id FROM threads WHERE (post_date BETWEEN '2021-08-02 00:00:00' AND '2021-08-05 11:59:59'))
GROUP BY word 
ORDER BY total_occurences
DESC LIMIT 200;

-- Get top 200 words across entire table
SELECT word, SUM(occurences) as total_occurences 
FROM words
GROUP BY word 
ORDER BY total_occurences
DESC LIMIT 200;

-- Get single word occurences over entire table
SELECT word, SUM(occurences) as total_occurences 
FROM words
WHERE word='x'
GROUP BY word 
ORDER BY total_occurences;

-- Get the size of the tables
SELECT
  TABLE_NAME AS `Table`,
  ROUND(((DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024),2) AS `Size (MB)`
FROM
  information_schema.TABLES
WHERE
  TABLE_SCHEMA = "archive_no_stopwords"
ORDER BY
  (DATA_LENGTH + INDEX_LENGTH)
DESC;



-- counts
select count(*) from threads;
select count(*) from words;
