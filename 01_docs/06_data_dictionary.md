# Data Dictionary
## Sephora Case 3 — Brand Affinity Detection

### Purpose
This document defines every variable within the `BDD#7_Database_Albert_School_Sephora.csv` dataset (~400,000 transaction rows, 34 columns) according to the official business rules provided in the Sephora Kick-off Deck.

### Relevance Definitions
- **Core:** Essential features for basket analysis, brand affinity, and Case 3 modeling.
- **Secondary:** Useful for filtering, context, or business-rule ranking.
- **Hold for later evaluation:** Usage depends on exploratory findings; may or may not improve recommendation logic.
- **Administrative / likely not used:** Technical IDs or fields irrelevant to brand affinity and discovery.

---

### 1. Customer & Profile Level
*Base identity, loyalty, and demographic data.*

| Column Name | Data Type | Null % | Business Meaning | Case 3 Relevance |
|---|---|---|---|---|
| `anonymized_card_code` | float64 | 0.00% | Hashed ID to identify unique customers across purchases. | **Core** |
| `status` | int64 | 0.00% | Loyalty status at the moment of purchase: 1 = No Fid, 2 = BRONZE, 3 = SILVER, 4 = GOLD. | **Core** |
| `RFM_Segment_ID` | int64 | 0.00% | Recency, Frequency, Amount segment at the end of the previous month. Segments 1, 2, 3 are the most valuable/engaged. | **Core** |
| `gender` | int64 | 0.00% | Customer's gender (1 = Men / 2 = Women). | **Secondary** |
| `age` | int64 | 0.00% | Customer's age (note: 0 likely means unknown). | **Secondary** |
| `age_category` | object | 28.01% | Customer's age category (high nulls correspond to missing/0 ages). | **Hold for later evaluation** |
| `age_generation` | object | 29.33% | Customer's age generation (e.g., Gen Z). | **Hold for later evaluation** |
| `subscription_date` | object | 1.41% | Date the customer subscribed to the loyalty program. | **Hold for later evaluation** |
| `subscription_store_code` | float64 | 74.07% | Store code where the customer subscribed. | **Hold for later evaluation** |
| `countryIsoCode` | object | 0.00% | Country of purchase. | **Administrative / likely not used** |
| `customer_city` | object | 3.96% | Declared city of residence. | **Administrative / likely not used** |

---

### 2. Transaction & Basket Level
*Purchase event mechanics (volume, spend, discounting, and channel).*

| Column Name | Data Type | Null % | Business Meaning | Case 3 Relevance |
|---|---|---|---|---|
| `anonymized_Ticket_ID` | float64 | 0.00% | Hashed transaction ID. Used to group products into baskets. | **Core** |
| `transactionDate` | object | 0.00% | Invoice date characterizing when the basket was purchased. | **Core** |
| `salesVatEUR` | float64 | 0.00% | Amount spent in EUR (turnover). | **Core** |
| `quantity` | int64 | 0.00% | Quantity of products purchased in this line item. | **Core** |
| `discountEUR` | float64 | 0.00% | Discount applied in EUR, crucial for discount-dependence logic. | **Core** |
| `channel` | object | 0.00% | 'estore' or 'store'. *Rule:* Appears 'estore' but store name isn't ESTORE = Click & Collect. | **Secondary** |
| `store_type_app` | object | 0.00% | App channel declination: APP / CSC / ESTORE / MOBILE / STORE / WEB. | **Secondary** |
| `store_code_name` | object | 0.00% | Association of the store code and name. | **Secondary** |
| `store_city` | object | 0.00% | City of the store. | **Administrative / likely not used** |

---

### 3. Product & Brand Level
*Item attributes identifying the affinity targets.*

| Column Name | Data Type | Null % | Business Meaning | Case 3 Relevance |
|---|---|---|---|---|
| `brand` | object | 1.54% | The brand of the product purchased. | **Core** |
| `Market_Desc` | object | 1.59% | SELECTIVE (sold everywhere), EXCLUSIVE (only at Sephora), SEPHORA (Sephora Collection). | **Core** |
| `Axe_Desc` | object | 0.00% | Product category: Make Up, Skincare, Fragrance, Haircare, Others. | **Core** |
| `materialCode` | int64 | 0.00% | Product ID. Kept because Case 3 may involve product-level similarity. | **Secondary** |

---

### 4. First Purchase / Acquisition Level
*Historical acquisition data. ~74% missing values. Missingness logic to be validated via EDA.*

| Column Name | Data Type | Null % | Business Meaning | Case 3 Relevance |
|---|---|---|---|---|
| `first_purchase_dt` | object | 74.07% | Date the cardholder made their first purchase. | **Hold for later evaluation** |
| `brand_first_purchase` | object | 74.07% | List of brands bought on the first purchase. | **Hold for later evaluation** |
| `channel_recruitment` | object | 74.07% | Channel used for the first purchase. | **Hold for later evaluation** |
| `Axe_Desc_first_purchase` | object | 74.07% | List of axes bought on the first purchase. | **Hold for later evaluation** |
| `Market_Desc_first_purchase` | object | 74.08% | List of markets bought on the first purchase. | **Hold for later evaluation** |
| `salesVatEUR_first_purchase` | float64 | 74.07% | Spending on first purchase. | **Hold for later evaluation** |
| `discountEUR_first_purchase` | float64 | 74.07% | Discount on first purchase. | **Hold for later evaluation** |
| `quantity_first_purchase` | float64 | 74.07% | Quantity on first purchase. | **Hold for later evaluation** |
| `materialCode_first_purchase`| object | 74.07% | Product IDs of first purchase. | **Hold for later evaluation** |
| `anonymized_first_purchase_id`| float64 | 74.07% | Hashed ticket ID of the first transaction. | **Administrative / likely not used** |
