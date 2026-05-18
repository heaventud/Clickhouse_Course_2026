## JOINs in Clickhouse

1. Match all movies with their genres

```sql
SELECT
    m.name,
    g.genre
FROM movies AS m
INNER JOIN genres AS g ON m.id = g.movie_id
;
```
2. Select all movies that don't have a genre

```sql
SELECT
    m.id,
    m.name,
    m.year
FROM movies AS m
LEFT JOIN genres AS g ON m.id = g.movie_id
WHERE g.genre = ''
;
```
3. Join all rows in movies table with rows in genres table

```sql
SELECT
    m.id,
    m.name,
    m.year,
    g.movie_id,
    g.genre
FROM movies AS m
CROSS JOIN genres AS g;
```
4. Match movies with their genres not using JOINs

```sql
SELECT
    m.name,
    g.genre
FROM movies AS m
LEFT JOIN genres AS g ON m.id = g.movie_id
WHERE g.genre != ''
;
```
5. Select all actors/actresses that played in N year

```sql
WITH roles_in_N_year AS
    (
        SELECT DISTINCT r.actor_id
        FROM roles AS r
        INNER JOIN movies AS m ON r.movie_id = m.id
        WHERE m.year = 2007
    )
SELECT
    ac.first_name,
    ac.last_name
FROM actors AS ac
SEMI LEFT JOIN roles_in_N_year ON ac.id = roles_in_N_year.actor_id
;
```
6. Use ANTI JOIN to find movies that don't have a genre

```sql
SELECT
    m.name,
    g.genre,
    m.year,
    m.rank
FROM movies AS m
ANTI LEFT JOIN genres AS g ON m.id = g.movie_id
;
```

#### Demo

![Terminal](./task_7.gif)
