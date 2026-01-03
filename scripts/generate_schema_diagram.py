"""
Generate database schema diagram from SQLAlchemy models
This script automatically generates Mermaid ERD diagram from the models
"""
import sys
import re
from pathlib import Path
from typing import List, Tuple

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def parse_model_file() -> List[Tuple[str, List[Tuple[str, str, bool, bool]]]]:
    """
    Parse models.py file to extract table and column information
    Returns: List of (table_name, [(column_name, type, is_pk, is_fk), ...])
    """
    models_file = Path(__file__).parent.parent / "app" / "db" / "models.py"
    
    if not models_file.exists():
        raise FileNotFoundError(f"Models file not found: {models_file}")
    
    with open(models_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    tables = []
    
    # Find all class definitions
    class_pattern = r'class\s+(\w+)\s*\([^)]+\):\s*"""[^"]*"""\s*__tablename__\s*=\s*"([^"]+)"'
    classes = re.finditer(class_pattern, content, re.MULTILINE | re.DOTALL)
    
    for class_match in classes:
        class_name = class_match.group(1)
        table_name = class_match.group(2)
        
        # Find the class body
        class_start = class_match.end()
        # Find next class or end of file
        next_class = content.find("\nclass ", class_start)
        if next_class == -1:
            class_body = content[class_start:]
        else:
            class_body = content[class_start:next_class]
        
        columns = []
        
        # Find all Column definitions
        column_pattern = r'(\w+)\s*=\s*Column\(([^)]+)\)'
        column_matches = re.finditer(column_pattern, class_body)
        
        for col_match in column_matches:
            col_name = col_match.group(1)
            col_def = col_match.group(2)
            
            # Determine type
            if "Integer" in col_def and "primary_key" in col_def:
                col_type = "int"
                is_pk = True
            elif "Integer" in col_def:
                col_type = "int"
                is_pk = False
            elif "String" in col_def:
                col_type = "string"
                is_pk = "primary_key" in col_def
            elif "Float" in col_def:
                col_type = "float"
                is_pk = "primary_key" in col_def
            elif "DateTime" in col_def:
                col_type = "datetime"
                is_pk = "primary_key" in col_def
            elif "Text" in col_def:
                col_type = "text"
                is_pk = "primary_key" in col_def
            elif "Boolean" in col_def:
                col_type = "boolean"
                is_pk = "primary_key" in col_def
            else:
                col_type = "string"
                is_pk = "primary_key" in col_def
            
            # Check for foreign key reference
            is_fk = "prediction_id" in col_name or "FK" in col_def or "Reference" in col_def
            
            columns.append((col_name, col_type, is_pk, is_fk))
        
        tables.append((class_name, columns))
    
    return tables


def get_column_info_parsed(table_name: str, columns: List[Tuple[str, str, bool, bool]]) -> List[str]:
    """Format column information for Mermaid"""
    formatted = []
    for col_name, col_type, is_pk, is_fk in columns:
        pk_mark = " PK" if is_pk else ""
        fk_mark = " FK" if is_fk else ""
        formatted.append(f"        {col_type} {col_name}{pk_mark}{fk_mark}")
    return formatted


def generate_detailed_mermaid():
    """Generate detailed Mermaid diagram"""
    try:
        tables = parse_model_file()
    except Exception as e:
        print(f"Error parsing models: {e}")
        # Fallback to manual definition
        return generate_fallback_mermaid()
    
    mermaid_lines = ["erDiagram"]
    
    for table_name, columns in tables:
        formatted_columns = get_column_info_parsed(table_name, columns)
        mermaid_lines.append(f"    {table_name} {{")
        mermaid_lines.extend(formatted_columns)
        mermaid_lines.append("    }")
        mermaid_lines.append("")
    
    # Relationships
    mermaid_lines.append("    Prediction ||--o{ PredictionLog : \"references\"")
    
    return "\n".join(mermaid_lines)


def generate_fallback_mermaid():
    """Fallback Mermaid diagram if parsing fails"""
    return """erDiagram
    StockData {
        int id PK
        string symbol
        datetime date
        float open
        float high
        float low
        float close
        int volume
        datetime created_at
    }
    
    Prediction {
        int id PK
        string symbol
        string model_name
        float predicted_price
        float confidence
        datetime prediction_date
        datetime created_at
    }
    
    PredictionLog {
        int id PK
        string symbol
        string model_name
        int prediction_id FK
        float predicted_price
        float actual_price
        float error_rate
        datetime prediction_date
        datetime actual_date
        boolean is_evaluated
        datetime created_at
        datetime updated_at
    }
    
    NewsLog {
        int id PK
        string symbol
        string title
        string link
        text summary
        datetime published_date
        float sentiment_score
        string sentiment_label
        string source
        datetime collected_at
    }
    
    PaperInsight {
        int id PK
        string paper_title
        string paper_doi
        string symbol
        text insight_summary
        text methodology
        text key_findings
        boolean is_read
        datetime created_at
    }
    
    Prediction ||--o{ PredictionLog : "references"
"""


def main():
    """Main function to generate schema diagram"""
    print("Generating database schema diagram...")
    
    # Generate Mermaid ERD
    mermaid_diagram = generate_detailed_mermaid()
    
    # Save to file
    output_file = Path(__file__).parent.parent / "docs" / "SCHEMA_AUTO.md"
    output_file.parent.mkdir(exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Database Schema Diagram (Auto-generated)\n\n")
        f.write("> ⚠️ This file is auto-generated. Edit `scripts/generate_schema_diagram.py` to modify.\n\n")
        f.write("## Entity Relationship Diagram\n\n")
        f.write("```mermaid\n")
        f.write(mermaid_diagram)
        f.write("\n```\n")
    
    print(f"✅ Schema diagram generated: {output_file}")
    print("\nTo view the diagram:")
    print("1. Open the file in a Markdown viewer that supports Mermaid (GitHub, GitLab, VS Code)")
    print("2. Or use online Mermaid editor: https://mermaid.live/")


if __name__ == "__main__":
    main()

