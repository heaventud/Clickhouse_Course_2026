## MergeTree Family engines

1. 

```sql
CREATE TABLE tbl1
(
    UserID UInt64,
    PageViews UInt8,
    Duration UInt8,
    Sign Int8,
    Version UInt8
)
ENGINE = VersionedCollapsingMergeTree(Sign, Version)
ORDER BY UserID;
```

2.

```sql
CREATE TABLE tbl2
(
    key UInt32,
    value UInt32
)
ENGINE = SummingMergeTree(value)
ORDER BY key;
```

3.

```sql
CREATE TABLE tbl3
(
    `id` Int32,
    `status` String,
    `price` String,
    `comment` String
)
ENGINE = ReplacingMergeTree
PRIMARY KEY (id)
ORDER BY (id, status);
```

4.

```sql
CREATE TABLE tbl4
(   CounterID UInt8,
    StartDate Date,
    UserID UInt64
) ENGINE = MergeTree
PARTITION BY toYYYYMM(StartDate)
ORDER BY (CounterID, StartDate);
```

5.

```sql
CREATE TABLE tbl5
(   CounterID UInt8,
    StartDate Date,
    UserID AggregateFunction(uniq, UInt64)
) ENGINE = AggregatingMergeTree
PARTITION BY toYYYYMM(StartDate)
ORDER BY (CounterID, StartDate);
```
6.

```sql
CREATE TABLE tbl6
(
    id Int32,
    status String,
    price String,
    comment String,
    Sign Int8
)
ENGINE = CollapsingMergeTree(Sign)
PRIMARY KEY (id)
ORDER BY (id, status);
```

#### Demo
![console](./task_6.gif)
