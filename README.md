# 📊 Customer Order Analytics Project — Interactive README

This **interactive-style README** includes expandable sections, structured documentation, and deployment guides — perfect for GitHub and project submissions.

---

# ✅ Overview

A complete data engineering + analytics project involving:

* Daily ETL pipeline (CSV + XML → Supabase)
* Cleaned & validated ingestion
* KPI SQL Views
* Streamlit Dashboard (tables left, graphs right)
* Automated scheduling (GitHub Actions)
* Security best practices

---

# ✅ 📁 Project Structure

```
project/
│── etl_pipeline.py
│── Load.py
│── dashboard.py
│── requirements.txt
│── data/ (input files)
│── .github/workflows/etl_daily.yml
│── README.md
```

---

# 📦 Features

✔ Automated daily ingestion using GitHub Actions
✔ Supabase-backed KPI views
✔ Streamlit dashboard (responsive & interactive)
✔ Secure secrets handling
✔ Chunked uploads & timestamp normalization
✔ Clean architecture with modular ETL components

---

# 🔄 ETL Pipeline  

<details>
<summary><strong>Click to expand</strong></summary>

### ETL Steps

1. **Extract** CSV + XML
2. **Transform** timestamps, numeric values, missing values
3. **Load** into Supabase with chunked upserts

### Run Locally

```
python etl_pipeline.py
```

### Daily Automation (GitHub Actions)

Your `.github/workflows/etl_daily.yml` triggers ETL daily:

```
on:
  schedule:
    - cron: "0 2 * * *"
```

</details>

---

# 🗄 Database Schema  

<details>
<summary><strong>Click to expand schema</strong></summary>

### customers

```
customer_id (PK)
customer_name
mobile_number
region
ingested_at
```

### orders

```
order_id (PK)
mobile_number
customer_id
order_date_time
sku_id
sku_count
total_amount
ingested_at
```

Indexes include:

* mobile_number
* order_date_time
* customer_id

</details>

---

# 📊 KPI SQL Views (Interactive)

<details>
<summary><strong>Repeat Customers</strong></summary>

```sql
CREATE OR REPLACE VIEW vw_repeat_customers AS
SELECT c.customer_id, c.customer_name,
       COUNT(o.order_id) AS orders_count
FROM customers c
JOIN orders o ON o.mobile_number = c.mobile_number
GROUP BY c.customer_id, c.customer_name
HAVING COUNT(o.order_id) > 1
ORDER BY orders_count DESC;
```

</details>

<details>
<summary><strong>Monthly Order Trends</strong></summary>

```sql
CREATE OR REPLACE VIEW vw_monthly_order_trends AS
SELECT to_char(date_trunc('month', order_date_time), 'YYYY-MM') AS month,
       COUNT(*) AS total_orders,
       SUM(total_amount) AS total_revenue
FROM orders
GROUP BY 1
ORDER BY 1;
```

</details>

<details>
<summary><strong>Regional Revenue</strong></summary>

```sql
CREATE OR REPLACE VIEW vw_regional_revenue AS
SELECT c.region, SUM(o.total_amount) AS revenue
FROM orders o
LEFT JOIN customers c ON c.mobile_number = o.mobile_number
GROUP BY c.region
ORDER BY revenue DESC;
```

</details>

<details>
<summary><strong>Top Spenders (Last 30 Days)</strong></summary>

```sql
CREATE OR REPLACE VIEW vw_top_spenders_last_30 AS
SELECT c.customer_id, c.customer_name,
       SUM(o.total_amount) AS total_spend,
       COUNT(o.order_id) AS order_count
FROM orders o
LEFT JOIN customers c ON o.mobile_number = c.mobile_number
WHERE o.order_date_time >= (NOW() - INTERVAL '30 days')
GROUP BY c.customer_id, c.customer_name
ORDER BY total_spend DESC
LIMIT 20;
```

</details>

---

# 🖥 Streamlit Dashboard  

<details>
<summary><strong>Click to view dashboard design</strong></summary>

### Run Streamlit

```
streamlit run dashboard.py
```

# 🚀 Deployment Link

live deployed Streamlit app:
👉 **[https://your-deployment-url-here]([https://your-deployment-url-here](https://akasaairdataengineering-k847bmmeexesbhtp7ceqjz.streamlit.app/))**


---

Use this README as your GitHub documentation.
