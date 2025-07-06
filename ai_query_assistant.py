import pandas as pd
import os
import sqlite3
from openai import OpenAI
from sqlalchemy import create_engine, text
import streamlit as st

# Configuration - Use Streamlit secrets in production
try:
    API_KEY = st.secrets["OPENAI_API_KEY"]
except:
    # Fallback for local development
    API_KEY = 'your-local-api-key-here'

class AIQueryAssistant:
    def __init__(self, csv_file_path="partial_csv.csv", api_key=None):
        """
        Initialize the AI Query Assistant
        
        Args:
            csv_file_path (str): Path to the CSV file
            api_key (str): OpenRouter API key (optional, uses default if not provided)
        """
        self.csv_file_path = csv_file_path
        self.api_key = api_key or API_KEY
        self.engine = None
        self.df = None
        self.client = None
        
        # Initialize components
        self._setup_client()
        self._setup_database()
    
    def _setup_client(self):
        """Setup OpenAI client for OpenRouter"""
        try:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url="https://openrouter.ai/api/v1"
            )
            print("✅ OpenAI client initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize OpenAI client: {e}")
            raise
    
    def _setup_database(self):
        """Load CSV and create SQLite database"""
        try:
            # Read CSV file
            self.df = pd.read_csv(self.csv_file_path, parse_dates=["sale_date"])
            print(f"✅ Loaded CSV with {len(self.df)} records")
            
            # Create SQLite database in memory
            self.engine = create_engine("sqlite:///sales.db")
            
            # Save DataFrame to SQLite
            self.df.to_sql("sales", self.engine, if_exists="replace", index=False)
            print("✅ Database setup completed")
            
        except FileNotFoundError:
            print(f"❌ Could not find '{self.csv_file_path}'. Please ensure the file exists.")
            raise
        except Exception as e:
            print(f"❌ Database setup failed: {e}")
            raise
    
    def _generate_sql_query(self, question):
        """Generate SQL query using OpenAI/OpenRouter"""
        
        prompt = f"""
You are an expert AI assistant that generates **accurate SQL queries for SQLite** databases based on user 
questions in plain English. 
You are working with the following table:

**Table: sales**

| Column Name             | Description                                     |
|-------------------------|-------------------------------------------------|
| sale_date               | Date of the sale (format: YYYY-MM-DD)          |
| customer_name           | Full name of the customer                       |
| customer_category       | Type of customer (e.g., 'Local', 'Export')      |
| customer_company_size   | Size of the customer's company (e.g., 'Small')  |
| satisfaction_rating     | Rating from 1 to 5                              |
| discount_offered        | 'Yes' or 'No'                                   |
| discount_amount_percent | Discount percentage (integer)                  |
| product_name            | Name of the product                             |
| base_price_per_ton      | Price per ton before discount (integer)        |
| warehouse_name          | Warehouse name                                  |
| warehouse_region        | Region of warehouse (e.g., 'North')             |
| final_tons_sold         | Final tons sold (float)                         |
| sale_amount             | Final sale amount in currency (float)           |

🧠 **Rules for Generating SQL**:
- Use **`customer_category`** when the user mentions customer type like 'Local' or 'Online' or 'International'
- Use **`customer_company_size`** for company size like 'Small', 'Medium', 'Large' or 'Mega'
- Use **`final_tons_sold`** if the user refers to "tons" or "tonnes" sold
- Always filter dates using `sale_date`
- Assume SQLite syntax
- Return **only the SQL query**, no explanations
- For **`customer_name`**, you can assume that the user may sometimes not be fully sure of the name, in that case use the LIKE operator. For example, the user might say that they need sales for customer that is named something like Downtown Grains
- Use proper SQL formatting and syntax
- Add LIMIT 100 to prevent overly large results unless specifically asked for all results

Now, generate a SQL query for the following user question:

**User question:** "{question}"

Return only the SQL query, nothing else.
"""

        try:
            response = self.client.chat.completions.create(
                model="mistralai/devstral-small:free",
                messages=[
                    {"role": "system", "content": "You are a SQL expert. Return only SQL queries, no explanations."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0
            )
            
            sql_query = response.choices[0].message.content.strip()
            
            # Clean up the SQL query
            if sql_query.startswith("```sql"):
                sql_query = sql_query[6:]
            if sql_query.startswith("```"):
                sql_query = sql_query[3:]
            if sql_query.endswith("```"):
                sql_query = sql_query[:-3]
            
            return sql_query.strip()
        
        except Exception as e:
            print(f"❌ Failed to generate SQL query: {e}")
            return None
    
    def _execute_sql_query(self, sql_query):
        """Execute SQL query and return results"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(sql_query))
                df_result = pd.DataFrame(result.fetchall(), columns=result.keys())
                return df_result, None
        except Exception as e:
            return None, str(e)
    
    def query(self, question, verbose=True):
        """
        Main method to ask a question and get results
        
        Args:
            question (str): Natural language question
            verbose (bool): Whether to print progress messages
            
        Returns:
            dict: Contains 'sql', 'result', 'error' keys
        """
        if verbose:
            print(f"\n🤔 Question: {question}")
        
        # Generate SQL
        if verbose:
            print("🧠 Generating SQL query...")
        sql_query = self._generate_sql_query(question)
        
        if not sql_query:
            return {
                'sql': None,
                'result': None,
                'error': 'Failed to generate SQL query'
            }
        
        if verbose:
            print(f"🔧 Generated SQL:\n{sql_query}")
        
        # Execute SQL
        if verbose:
            print("⚡ Executing query...")
        df_result, error = self._execute_sql_query(sql_query)
        
        if error:
            if verbose:
                print(f"❌ Query execution failed: {error}")
            return {
                'sql': sql_query,
                'result': None,
                'error': error
            }
        else:
            if verbose:
                print(f"✅ Query successful! Returned {len(df_result)} rows")
                print("\n📊 Results:")
                print(df_result)
            return {
                'sql': sql_query,
                'result': df_result,
                'error': None
            }
    
    def run_interactive(self):
        """Run interactive command-line interface"""
        print("🤖 Welcome to the AI Query Assistant!")
        print("Type your SQL queries in natural language. Type 'exit' to quit.\n")
        print("Example questions:")
        print("- What is the total sale amount for 2024?")
        print("- What are total sales?")
        print("- Show me sales for customer named Downtown Grains")
        print("- How many tons were sold in the North region?")
        print("-" * 50)
        
        while True:
            try:
                question = input("\n💭 What is your query? ")
                
                if question.lower() in ["exit", "quit", "n"]:
                    print("👋 Goodbye!")
                    break
                
                if not question.strip():
                    print("⚠️ Please enter a question.")
                    continue
                
                # Run query
                result = self.query(question, verbose=True)
                
                if result['error']:
                    print(f"\n❌ Error: {result['error']}")
                    print("💡 Try rephrasing your question or check the column names.")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Unexpected error: {e}")

# Convenience functions for backward compatibility
def run_sql(question, csv_file="partial_csv.csv", api_key=None, verbose =True):
    """
    Backward compatibility function
    
    Args:
        question (str): Natural language question
        csv_file (str): Path to CSV file
        api_key (str): API key (optional)
        
    Returns:
        pandas.DataFrame: Query results
    """
    assistant = AIQueryAssistant(csv_file, api_key)
    result = assistant.query(question, verbose=verbose)
    
    if result['error']:
        print(f"❌ Error: {result['error']}")
        return None
    
    return result['result']

def run():
    """Backward compatibility function for interactive mode"""
    assistant = AIQueryAssistant()
    assistant.run_interactive()

# Main execution
if __name__ == "__main__":
    # Create assistant and run interactive mode
    assistant = AIQueryAssistant()
    assistant.run_interactive()
