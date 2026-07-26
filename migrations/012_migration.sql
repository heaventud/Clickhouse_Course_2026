CREATE TABLE default.user_activity
(
    user_id UInt32,
    activity_type String,
    activity_date DateTime
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(activity_date)
;
