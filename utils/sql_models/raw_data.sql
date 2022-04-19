CREATE SCHEMA IF NOT EXISTS raw;
DROP TABLE IF EXISTS raw.voucher_payment_hist;

CREATE TABLE IF NOT EXISTS raw.voucher_payment_hist
(
    timestamp TIMESTAMPTZ,
    country_code VARCHAR(30),
    last_order_ts  TIMESTAMPTZ,
	first_order_ts TIMESTAMPTZ,
    total_orders  float,
	voucher_amount float,
	diff_in_days  float
);