-- Core product information
CREATE TABLE products (
    product_id BIGINT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    brand_id BIGINT REFERENCES brands(brand_id),
    base_price DECIMAL(10,2) NOT NULL,
    current_price DECIMAL(10,2) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    active BOOLEAN DEFAULT TRUE
);

-- Product attributes (allowing for flexible attribute additions)
CREATE TABLE product_attributes (
    product_id BIGINT REFERENCES products(product_id),
    attribute_key VARCHAR(50),
    attribute_value TEXT,
    PRIMARY KEY (product_id, attribute_key)
);

-- Categories with hierarchical structure
CREATE TABLE categories (
    category_id BIGINT PRIMARY KEY,
    parent_category_id BIGINT REFERENCES categories(category_id),
    name VARCHAR(100) NOT NULL,
    level INT NOT NULL,
    path TEXT NOT NULL
);

-- Product category mappings (allowing products in multiple categories)
CREATE TABLE product_categories (
    product_id BIGINT REFERENCES products(product_id),
    category_id BIGINT REFERENCES categories(category_id),
    PRIMARY KEY (product_id, category_id)
);

-- Occasion mappings
CREATE TABLE occasions (
    occasion_id BIGINT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT
);

-- Product-occasion mappings with relevance scores
CREATE TABLE product_occasions (
    product_id BIGINT REFERENCES products(product_id),
    occasion_id BIGINT REFERENCES occasions(occasion_id),
    relevance_score DECIMAL(3,2),  -- 0 to 1 score for how appropriate the item is
    PRIMARY KEY (product_id, occasion_id)
);

-- Style profiles
CREATE TABLE style_profiles (
    style_id BIGINT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT
);

-- Product style mappings with confidence scores
CREATE TABLE product_styles (
    product_id BIGINT REFERENCES products(product_id),
    style_id BIGINT REFERENCES style_profiles(style_id),
    confidence_score DECIMAL(3,2),
    PRIMARY KEY (product_id, style_id)
);

-- Inventory tracking
CREATE TABLE inventory (
    product_id BIGINT REFERENCES products(product_id),
    size VARCHAR(50),
    color VARCHAR(50),
    quantity INT,
    warehouse_id BIGINT,
    PRIMARY KEY (product_id, size, color, warehouse_id)
);

-- User preferences and profiles
CREATE TABLE user_preferences (
    user_id BIGINT PRIMARY KEY,
    style_preferences JSONB,  -- Flexible storage for style preferences
    size_preferences JSONB,   -- Size preferences by category
    price_ranges JSONB,       -- Preferred price ranges by category
    color_preferences JSONB,  -- Color preferences
    brand_preferences JSONB,  -- Brand preferences/exclusions
    occasion_preferences JSONB -- Occasion-specific preferences
);

-- User interaction history
CREATE TABLE user_interactions (
    interaction_id BIGINT PRIMARY KEY,
    user_id BIGINT REFERENCES user_preferences(user_id),
    product_id BIGINT REFERENCES products(product_id),
    interaction_type VARCHAR(50),  -- view, purchase, save, etc.
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    context JSONB  -- Additional context about the interaction
);