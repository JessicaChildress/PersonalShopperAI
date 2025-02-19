# PersonalShopperAI

Creating a Personal Shopper AI Agent. Details TBD


## Brainstorming the Process

1) Data Foundations
    * Design clothing database schema
    * Start with synthetic data (fill using a data pipeline) for initial development
    * Add real data sources using retail APIs and web scraping
    * Enrich the data by adding occasion mappings and generating style profiles
2) Core Recommendation System
    * Build a content-based filtering system using item attributes
    * Implement occasion-based filtering ("casual summer party", "black tie wedding")
    * Create gift recommendation logic using recipient attributes like age, style and relationship
    * Add price range filtering and style matching
3) Natural Language Understanding (AI Agent) 
    * Develop parsing for user queries 
    * Extract key elements like occasion, budget, and style to use in queries
4) UI & UX 
    * Create a way to gather user preferences and constraints (dropdowns, check boxes, etc.)
    * Try to mimic the feel of navigating a clothing store only smooth the edges
    * Design a clear output format for the recommendations
    * Include an explanation for why item(s) were recommended
    * Allow for feedback and refinement of suggestions (can I build reinforcement learning into the user interactions?)
        > What if the UI was like a Buzzfeed quiz and the user selecet a series of images to inform the model of their style preferences? 
        > Potentially part of the account creation process? 
5) Evaluation & Testing
    * Define metrics for recommendation quality (what is a "good" recommendation? Does the user navigate to the site to make the purchase?)
        > Long term: is it possible to get a partnership like what bloggers have so I get a kickback when the recommendation works? Does that help or hurt the product? 
    * Test with diverse user scenarios (age, style, budget, occasion)
    * Define metrics for occasion matching quality (did the item match the occasion? Is this another instance where the user navigating to the page gives us our answer?)
    * Validate the price and style constraints (are all of the products assigned to the right bucket? )
        > Future concern: What if something is on sale right now?


### Scalable Clothing DataBase Schema `scalable_clothing_db_schema.sql`

Key considerations when designing a scalable database schema for this project include:
- Flexible Attribute System:
    * Products can have unlimited attributes without schema changes
    * Supports new fashion trends and product types easily
    * Enables efficient filtering and searching
- Hierarchical Categories:
    * Multi-level category structure (Clothing > Dresses > Casual Dresses)
    * Products can belong to multiple categories
    * Supports complex navigation and filtering
- Occasion and Style Mappings:
    * Products are mapped to occasions with relevance scores
    * Products can belong to style profiles
    * Enables nuanced recommendations
- User Preferences and History:
    * JSON fields for flexible preference storage
    * Detailed interaction tracking
    * Supports personalization at scale

### E-Commerce Data Pipeline `ecommerce_data_pipeline.py`

This pipeline was deesigned to efficiently populate the database with synthetic data. First, the pipeline will help generate realistic test data for the initial development of a working product. Then I will shift to adding real data sources using a multi-step approach that combines web scraping, API usage, and data processing. 
- Start with Synthetic Data:
    * Generate realistic test data using the pipeline
    * Great for initial development and testing 
    * Help validate schema and queries
    * Can generate thousands of records quickly
- Add Real Data Sources:
    * Scrape public fashion websites (staying within the legal data limits of course)
    * Use retail APIs like Shopify API, Amazon Product API, and H&M API
    * Parse product catalogs from open datasets 
    * Use a vision model to learn styles by passing in images from fashion magazines/blogs across a variety of time periods and styles
- Enrich the Data:
    * Add occasion mappings
    * Generate style profiles
