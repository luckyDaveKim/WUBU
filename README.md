# WUBU
우리 부자되자

# 초기화 쿼리
## DB 생성
```sql
CREATE DATABASE IF NOT EXISTS `investar` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
```

## Table 생성
```sql
CREATE TABLE IF NOT EXISTS company_info
(
    id          varchar(20) not null primary key,
    name        varchar(40) null,
    last_update date        null
)

CREATE TABLE IF NOT EXISTS daily_price
(
    company_id varchar(20) not null,
    date       date        not null,
    open       bigint      null,
    high       bigint      null,
    low        bigint      null,
    close      bigint      null,
    primary key (company_id, date)
)

CREATE TABLE IF NOT EXISTS daily_volume
(
    company_id varchar(20) not null,
    date       date        not null,
    volume     bigint      null,
    primary key (company_id, date)
)
```

```sql
CREATE TABLE IF NOT EXISTS favorite_company
(
    id         bigint      not null AUTO_INCREMENT PRIMARY KEY,
    company_id varchar(20) not null
)

CREATE TABLE IF NOT EXISTS minutely_price
(
    company_id varchar(20) not null,
    datetime   datetime    not null,
    open       bigint      null,
    high       bigint      null,
    low        bigint      null,
    close      bigint      null,
    primary key (company_id, datetime)
)

CREATE TABLE IF NOT EXISTS minutely_volume
(
    company_id varchar(20) not null,
    datetime   datetime    not null,
    volume     bigint      null,
    primary key (company_id, datetime)
)

CREATE TABLE IF NOT EXISTS daily_exchange_rate
(
    date date   not null,
    rate double null,
    primary key (date, rate)
)

CREATE TABLE IF NOT EXISTS minutely_exchange_rate
(
    datetime datetime not null,
    rate     double   null,
    primary key (datetime, rate)
)
```

# 사용법
```bash
> cd src/config/
> python DBUpdater.py
```